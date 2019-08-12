from random import randint
from util import *
from BagCrypto import *

class AttckBag(object):
    def __init__(self):
        self.pub = []
        self.pri = []
        self.m = None
        self.w = None
        self.revW = None

    def setPub(self, pub):
        self.pub = pub

    def attack(self):
        su = 0
        for i in self.pub:
            su += i
        while True:
            m = randint(su + 1, 2 * su)
            while True:
                w = randint(3, m - 1)
                r, tw, tm = extendEuclid(w, m)
                if r == 1:
                    self.w = w
                    if tw < 0:
                        tw += m
                    self.revW = tw
                    self.m = m
                    break
            self.pri = [p * self.revW % self.m for p in self.pub]
            #self.pri = sorted(self.pri)
            s = 0
            flag = True
            for r in self.pri:
                if s >= r:
                    flag = False
                    break
                s += r
            if flag:
                break

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
    plain = int(input("Input plain number: "))
    length = len(bin(plain)[2:])
    b.generateKey(length)
    c = b.encrypt(plain)
    print("Cipher:")
    print(c)
    atk = AttckBag()
    atk.setPub(b.pub)
    atk.attack()
    p = atk.decrypt(c)
    print("Attack accomplished.")
    print("Private Key:")
    print(atk.pri)
    print("Plain:")
    print(p)