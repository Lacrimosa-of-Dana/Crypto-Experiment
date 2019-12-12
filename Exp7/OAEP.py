import hashlib
import sys
from random import randint
from util import MGF
class OAEP(object):
    # hashtype: sha-256

    def __init__(self):
        self.k = 128
        self.hLen = 32
        self.msg = None
        self.mLen = None
        self.EM = None

    def setM(self, msgList):
        self.mLen = len(msgList)
        if self.mLen > self.k - 2 * self.hLen - 2:
            print("Message block too long.")
            sys.exit(0)
        self.msg = ''.join(["%02x"%m for m in msgList])

    def setEM(self, EM):
        self.EM = EM

    def encode(self):
        lHash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        PS = "00" * (self.k - self.mLen - 2 * self.hLen - 2)
        DB = lHash + PS + "01" + self.msg
        seed = ("%0" + str(2 * self.hLen) + "x")%(randint(1 << (8 * self.hLen) - 1, (1 << (8 * self.hLen)) - 1))
        dbMask = MGF(seed, self.k - self.hLen - 1)
        maskDB = ("%0" + str(2 * (self.k - self.hLen - 1)) + "x")%(int(DB, 16) ^ int(dbMask, 16))
        seedMask = MGF(maskDB, self.hLen)
        maskedSeed = ("%0" + str(2 * self.hLen) + "x")%(int(seed, 16) ^ int(seedMask, 16))
        self.EM = "00" + maskedSeed + maskDB
    def decode(self):
        lHash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        maskedSeed = self.EM[2:2+2*self.hLen]
        maskDB = self.EM[2+2*self.hLen:]
        seedMask = MGF(maskDB, self.hLen)
        seed = ("%0" + str(2 * self.hLen) + "x")%(int(maskedSeed, 16) ^ int(seedMask, 16))
        dbMask = MGF(seed, self.k - self.hLen - 1)
        DB = int(maskDB, 16) ^ int(dbMask, 16)
        temp = (("%0" + str(2 * (self.k - self.hLen - 1)) + "x")%DB)[2*self.hLen:]
        while temp[0:2] != "01":
            temp = temp[2:]
        self.msg = temp[2:]

    def getEM(self):
        return self.EM

    def getM(self):
        return self.msg

if __name__ == '__main__':
    test = OAEP()
    test.setM([1, 2, 3])
    test.encode()
    print(test.getEM())
    test.decode()
    print(test.getM())    
