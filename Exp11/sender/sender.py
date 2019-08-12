import os
from socket import *
from gmssl import sm4
import sys
sys.path.append("../sm2")
import SM2Sign
from random import randint
from util import *
from ECCPoint import *

class Sender(object):
    def __init__(self, sid):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(("127.0.0.1", 1024))
        self.id = sid
        self.public = None
        self.private = None
        self.key = None
        self.iv = (0x000102030405060708090a0b0c0d0e0f).to_bytes(16, byteorder='big')

    def generateKey(self):
        self.private = randint(3, ECCPoint.n - 1)
        self.public = SM2Sign.SM2Sign.g.multi(self.private)   

    def decideKey(self, sock, auth):
        sign = SM2Sign.SM2Sign(self.id)
        sign.public = self.public
        sign.private = self.private
        k = randint(3, ECCPoint.n - 1)
        pt = point_to_bytes(SM2Sign.SM2Sign.g.multi(k))
        sig = sign.sign(pt)
        sock.send(b''.join([pt, sig[0], sig[1]]))
        other = sock.recv(130)
        otherPt = bytes_to_point(other[:65])
        otherSig = other[65:]
        if not auth.authenticate(other[:65], (otherSig[:32], otherSig[32:])):
            print("Authentication failed while key exchanging.")
            self.sock.close()
            sys.exit(0)
        self.key = point_to_bytes(otherPt.multi(k))[1:]
        #print(self.key)

    def encryptFile(self, addr):
        with open(addr, "rb") as f:
            src = f.read()
        name = os.path.split(addr)[1].encode()
        sign = SM2Sign.SM2Sign(self.id)
        sign.public = self.public
        sign.private = self.private
        signature = sign.sign(src)
        encrypt = sm4.CryptSM4()
        encrypt.set_key(self.key, 0)
        encryptIV = encrypt.crypt_ecb(self.iv)
        cipher = encrypt.crypt_cbc(
            self.iv, b''.join([bytes([len(name)]), name, src, signature[0], signature[1]]))
        return b''.join([encryptIV, cipher])

    def sendFile(self, address):
        self.sock.listen(5)
        sock, addr = self.sock.accept()
        sock.send(self.id.encode())
        targetID = sock.recv(10).decode()
        auth = SM2Sign.SM2Sign(targetID)
        sock.send(point_to_bytes(self.public))
        auth.public = bytes_to_point(sock.recv(65))
        self.decideKey(sock, auth)
        e = self.encryptFile(address)
        sock.send((len(e)).to_bytes(3, byteorder='big'))
        for i in range(0, len(e), 1024):
            sock.send(e[i:i+1024])
        print("The file has been sent to " + targetID + ".")
        self.sock.close()
    
if __name__ == '__main__':
    while True:
        sid = input("Input sender ID (no more than 10 bytes): ")
        if len(sid) <= 10:
            break
        else:
            print("ID too long.")
    s = Sender(sid)
    s.generateKey()
    fileAddr = input("Input the file address: ")
    if not os.path.isfile(fileAddr):
        print("File dose not exist.")
        sys.exit(0)
    s.sendFile(fileAddr)