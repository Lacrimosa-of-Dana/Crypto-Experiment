from random import randint
from ECCPoint import *

class Client(object):
    g = ECCPoint(ECCPoint.xg, ECCPoint.yg)
    def __init__(self):
        self.private = None
        self.public = None
        self.sharedKey = None

    def generateKey(self):
        self.private = randint(2, ECCPoint.n - 1)
        self.public = Client.g.multi(self.private)

    def calcSharedKey(self, otherPublic):
        self.sharedKey = otherPublic.multi(self.private)

class ECCDH(object):
    def __init__(self, client1, client2):
        self.client1 = client1
        self.client2 = client2
        self.client1.generateKey()
        self.client2.generateKey()
        self.sharedKey = None

    def exchange(self):
        self.client1.calcSharedKey(self.client2.public)
        self.client2.calcSharedKey(self.client1.public)
        self.sharedKey = self.client1.sharedKey

if __name__ == '__main__':
    client1 = Client()
    client2 = Client()
    dh = ECCDH(client1, client2)
    dh.exchange()
    print(dh.sharedKey.outputPosition())
    print(client1.sharedKey.outputPosition())
    print(client2.sharedKey.outputPosition())
