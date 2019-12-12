from random import randint
from util import *

class BagCrypto(object):
    def __init__(self):
        self.pub = None
        self.pri = None
        self.w = None
        self.revW = None
        self.m = None

    def generateKey(self, len):
        self.pri = [1]
        s = 1
        for i in range(1, len):
            temp = randint(s + 1, 2 * s)
            s += temp
            self.pri.append(temp)
        self.m = randint(2 * self.pri[-1], 4 * self.pri[-1])
        while True:
            w = randint(3, self.m - 1)
            r, tw, tm = extendEuclid(w, self.m)
            if r == 1:
                if w < 0:
                    tw += self.m
                self.w = w
                self.revW = tw
                self.pub = [k * w % self.m for k in self.pri]
                break

    def encrypt(self, plain):
        cipher = 0
        p = bin(plain)[2:]
        for i in range(len(p)):
            if p[i] == '1':
                cipher += self.pub[i]
        return cipher

    def decrypt(self, cipher):
        plainList = []
        c = cipher * self.revW % self.m
        for i in range(len(self.pri) - 1, -1, -1):
            if c >= self.pri[i]:
                plainList.append('1')
                c -= self.pri[i]
            else:
                plainList.append('0')
        plainList.reverse()
        return int(''.join(plainList), 2)

if __name__ == '__main__':
    b = BagCrypto()
    plain = int(input("Plain number: "))
    length = len(bin(plain)[2:])
    b.generateKey(length)
    c = b.encrypt(plain)
    print("Cipher:")
    print(c)
    print("Decrypt Cipher into Plain:")
    print(b.decrypt(c))