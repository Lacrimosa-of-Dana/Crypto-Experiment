from random import randint
from ECCPoint import *

class ECCElGamal(object):
    g = ECCPoint(ECCPoint.xg, ECCPoint.yg)
    def __init__(self):
        self.public = None
        self.private = None
        self.plain = None
        self.cipher = None

    def setPlain(self, plain):
        self.plain = plain

    def setCipher(self, cipher):
        self.cipher = cipher

    def generateKey(self):
        self.private = randint(2, ECCPoint.n - 1)
        self.public = self.g.multi(self.private)

    def encrypt(self):
        k = randint(1, ECCPoint.n - 1)
        self.cipher = ECCElGamal.g.multi(k), self.plain + self.public.multi(k)

    def decrypt(self):
        self.plain = self.cipher[1] - self.cipher[0].multi(self.private)

if __name__ == '__main__':
    t = ECCElGamal()
    t.setPlain(ECCPoint(2, 3))
    t.generateKey()
    t.encrypt()
    print("Plain:")
    print(t.plain.outputPosition())
    print("Cipher:")
    print(t.cipher[0].outputPosition())
    print(t.cipher[1].outputPosition())
    t.decrypt()
    print("Decrypted Plain:")
    print(t.plain.outputPosition())
        
