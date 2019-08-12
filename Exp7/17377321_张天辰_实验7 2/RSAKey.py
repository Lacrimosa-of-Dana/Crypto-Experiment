from util import *

class RSAKey(object):
    def __init__(self):
        self.n = None
        self.e = None

    def generateKey(self):
        p = generatePrime()
        #while True:
        q = generatePrime()
        #    if p != q:
        #       break
        self.n = p * q
        phi = (p - 1) * (q - 1)
        self.e, d = generateED(phi)
        if d < 0:
            d += phi
        with open("public.txt", "w") as fpu:
            fpu.write(str(self.n) + '\n' + str(self.e))
        with open("private.txt", "w") as fpr:
            fpr.write(str(p) + '\n' + str(q) + '\n' + str(d))

if __name__ == '__main__':
    k = RSAKey()
    k.generateKey()