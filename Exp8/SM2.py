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

    def setPlain(self, plain):
        self.plain = plain

    def setCipher(self, cipher):
        self.cipher = cipher

    def generateKey(self):
        private = randint(3, ECCPoint.n - 1)
        with open("private.txt", "wb") as fpr:
            fpr.write(bytes(int_to_bytes(private, 32)))
        public = self.g.multi(private)
        with open("public.txt", "wb") as fpu:
            fpu.write(bytes(point_to_bytes(public)))

    @staticmethod
    def KDF(Z, klen):
        v = 256
        ct = 1
        hashList = []
        for i in range(ceil(klen / v)):
            temp = b''.join([Z + int_to_bytes(ct, 4)])
            hashList.append(bytes_to_int(hashlib.sha256(bytes(temp)).digest()))
            ct += 1
        hashList[-1] = (hashList[-1] >> (v - klen + v * (klen // v))) if klen % v != 0 else hashList[-1]
        k = 0
        for i in range(ceil(klen / v) - 1):
            k <<= v
            k += hashList[i]
        k <<= (klen - v * (klen // v))
        k += hashList[-1]
        return k
    
    def encrypt(self):
        with open("public.txt", "rb") as fpu:
            public = bytes_to_point(fpu.read())
        klen = len(self.plain)
        while True:
            k = randint(1, ECCPoint.n - 1)
            c1 = point_to_bytes(self.g.multi(k))
            pt = public.multi(k)
            x2 = elm_to_bytes(pt.x)
            y2 = elm_to_bytes(pt.y)
            t = self.KDF(b''.join([x2, y2]), 8 * klen)
            if t != 0:
                break
        #print(klen)
        #print(int_to_bytes(t, klen))
        c2 = int_to_bytes(bytes_to_int(self.plain) ^ t, klen)
        h = b''.join([x2, self.plain, y2])
        c3 = hashlib.sha256(bytes(h)).digest()
        self.cipher = b''.join([c1 + c3 + c2])
    
    def decrypt(self):
        with open("private.txt", "rb") as fpr:
            private = bytes_to_int(fpr.read())
        #cipher = c1(length=65) + c3(length=32) + c2(length=len(plain))
        klen = len(self.cipher) - 97
        c2 = self.cipher[-klen:]
        c3 = self.cipher[-32-klen:-klen]
        c1 = self.cipher[:-32-klen]

        test = bytes_to_point(c1)
        pt = test.multi(private)
        x2 = elm_to_bytes(pt.x)
        y2 = elm_to_bytes(pt.y)
        t = self.KDF(b''.join([x2, y2]), 8 * klen)
        if t == 0:
            print("Error raised in decrypting.")
            sys.exit(0)
        m = int_to_bytes(bytes_to_int(c2) ^ t, klen)
        u = hashlib.sha256(b''.join([x2, m, y2])).digest()
        if u != c3:
            print("Error raised in decrypting. Perhaps the cipher has been tampered.")
            sys.exit(0)
        self.plain = m

    def outputPlain(self):
        with open("Plain.txt", "wb") as fp:
            fp.write(self.plain)

    def outputCipher(self):
        with open("Cipher.txt", "wb") as fc:
            fc.write(self.cipher)
        
if __name__ == '__main__':
    SM2 = SM2()
    print("SM2 CRYPTO")
    print("=" * 20)
    gen = input("Generate keys? [Y/N]:")
    if gen == 'y' or gen == 'Y':
        SM2.generateKey()
    mode = input("Encrypt or Decrypt? [E/D]:")
    if mode == 'e' or mode == 'E':
        with open("Plain.txt", "rb") as fp:
            plain = fp.read()
        SM2.setPlain(plain)
        SM2.encrypt()
        SM2.outputCipher()
    elif mode == 'd' or mode == 'D':
        with open("Cipher.txt", "rb") as fc:
            cipher = fc.read()
        SM2.setCipher(cipher)
        SM2.decrypt()
        SM2.outputPlain()
    print("Mission accomplished.")
    print("=" * 20)



