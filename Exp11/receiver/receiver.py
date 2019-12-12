import os
from socket import *
from gmssl import sm4
import sys
sys.path.append("../sm2")
import SM2Sign
from random import randint
from ECCPoint import *
from util import *

class Receiver(object):
    def __init__(self, sid):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.id = sid
        self.public = None
        self.private = None
        self.key = None
        self.iv = None

    def generateKey(self):
        self.private = randint(3, ECCPoint.n - 1)
        self.public = SM2Sign.SM2Sign.g.multi(self.private)   

    def decideKey(self, auth):
        other = self.sock.recv(130)
        k = randint(3, ECCPoint.n - 1)
        otherPt = bytes_to_point(other[:65])
        otherSig = other[65:]
        if not auth.authenticate(other[:65], (otherSig[:32], otherSig[32:])):
            print("Authentication failed while key exchanging.")
            self.sock.close()
            sys.exit(0)
        self.key = point_to_bytes(otherPt.multi(k))[1:]
        #print(SM2Sign.SM2Sign.g.multi(k).outputPosition())
        sign = SM2Sign.SM2Sign(self.id)
        sign.public = self.public
        sign.private = self.private
        pt = point_to_bytes(SM2Sign.SM2Sign.g.multi(k))
        sig = sign.sign(pt)
        self.sock.send(b''.join([pt, sig[0], sig[1]]))
        #print(self.key)

    def receiveFile(self):
        self.sock.connect(("127.0.0.1", 1024))
        sid = self.sock.recv(10).decode()
        auth = SM2Sign.SM2Sign(sid)
        self.sock.send(self.id.encode())
        auth.public = bytes_to_point(self.sock.recv(65))
        self.sock.send(point_to_bytes(self.public))
        self.decideKey(auth)
        t = self.sock.recv(3)
        length = int.from_bytes(t, byteorder='big')
        l = 0
        target = b''
        while l < length:
            t = self.sock.recv(1024)
            target = b''.join([target, t])
            l += len(t)
        decrypt = sm4.CryptSM4()
        decrypt.set_key(self.key, 1)
        self.iv = decrypt.crypt_ecb(target[:32])
        target = decrypt.crypt_cbc(self.iv, target[32:])
        nameLen = target[0]
        name = target[1:1+nameLen]
        result = auth.authenticate(target[1+nameLen:-64], (target[-64:-32], target[-32:]))
        if result:
            with open(name.decode(), "wb") as f:
                f.write(target[1+nameLen:-64])
            print("File received from " + sid)
        else:
            print("Authentication failed while receiving.")
            self.sock.close()
            sys.exit(0)
        self.sock.close()

if __name__ == '__main__':
    while True:
        rid = input("Input sender ID (no more than 10 bytes): ")
        if len(rid) <= 10:
            break
        else:
            print("ID too long.")
    r = Receiver(rid)
    r.generateKey()
    r.receiveFile()
