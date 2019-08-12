from random import randint
from ECCPoint import *
from math import ceil
from util import *
import hashlib
import sys

class SM2(object):
    g = ECCPoint(ECCPoint.xg, ECCPoint.yg)
    def __init__(self):
        self.plain = None
        self.cipher = None
        self.public = None
        self.private = None

    def setPlain(self, plain):
        self.plain = plain

    def setCipher(self, cipher):
        self.cipher = cipher

    def setPublic(self):
        self.private = 0x3945208F7B2144B13F36E38AC6D39F95889393692860B51A42FB81EF4DF7C5B8
        self.public = self.g.multi(self.private)

    @staticmethod
    def KDF(Z, klen):
        v = 256
        ct = 1
        hashList = []
        for i in range(ceil(klen / v)):
            temp = Z + int_to_bytes(ct, 4)
            hashList.append(bytes_to_int(hashlib.sha256(bytes(temp)).digest()))
            ct += 1
        hashList[-1] = (hashList[-1] >> (v - klen + v * (klen // v))) if klen % v != 0 else hashList[-1]
        k = 0
        for i in range(ceil(klen / v)):
            k <<= v
            k += hashList[i]
        return k
    
    def encrypt(self):
        klen = len(self.plain)
        print(klen)
        while True:
            k = randint(1, ECCPoint.n - 1)
            c1 = point_to_bytes(self.g.multi(k))
            pt = self.public.multi(k)
            x2 = elm_to_bytes(pt.x)
            y2 = elm_to_bytes(pt.y)
            t = self.KDF(x2 + y2, 8 * klen)
            if t != 0:
                break
        c2 = int_to_bytes(bytes_to_int(self.plain) ^ t, klen)
        h = x2 + self.plain + y2
        c3 = list(hashlib.sha256(bytes(h)).digest())
        self.cipher = c1 + c3 + c2
    
    def decrypt(self):
        #cipher = c1(length=?) + c3(length=32) + c2(length=len(plain))
        #undefined klen
        klen = 12
        c2 = self.cipher[-klen:]
        c3 = self.cipher[-32-klen:-klen]
        c1 = self.cipher[:-32-klen]

        test = bytes_to_point(c1)
        pt = test.multi(self.private)
        x2 = elm_to_bytes(pt.x)
        y2 = elm_to_bytes(pt.y)
        t = self.KDF(x2 + y2, 8 * klen)
        if t == 0:
            print("Error raised in decrypting.")
            sys.exit(0)
        m = int_to_bytes(bytes_to_int(c2) ^ t, klen)
        u = list(hashlib.sha256(bytes(x2 + m + y2)).digest())
        if u != c3:
            print("Error raised in decrypting. Perhaps the cipher has been tampered.")
            sys.exit(0)
        self.plain = m
        
if __name__ == '__main__':
    s = SM2()
    print(s.KDF([1, 2, 3], 512))
    s.setPublic()
    s.setPlain(list("testcodegood".encode('utf-8')))
    s.encrypt()
    s.decrypt()
    print(s.plain)

