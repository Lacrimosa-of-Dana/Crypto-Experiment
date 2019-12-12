from OAEP import *
from util import *
class RSA(object):
    def __init__(self, address):
        with open("public.txt", "r") as f:
            keys = f.readlines()
        self.n = int(keys[0].strip())
        self.e = int(keys[1].strip())
        self.address = address
        self.msgList = None
        self.plainList = []
        self.cipherList = []
        self.OAEP = OAEP()

    def setMsg(self):
        self.msgList = []
        with open(self.address, "rb") as f:
            self.msgList = list(f.read())
        msgLen = len(self.msgList)
        padNum = msgLen % 60
        if padNum == 0:
            padNum += 60
        #print(padNum)
        padNum -= 1
        self.msgList += [0] * padNum
        self.msgList += [padNum]
        #print(self.msgList)
        msgLen = len(self.msgList)
        for i in range(0, msgLen, 60):
            self.plainList.append(self.msgList[i:i+60])
    
    def setCip(self):
        self.cipherList = []
        with open(self.address, "rb") as f:
            temp = list(f.read())
        tpLen = len(temp)
        for i in range(0, tpLen, 128):
            part = temp[i:i+128]
            self.cipherList.append(''.join(["%02x"%t for t in part]))
        #print(self.cipherList)

    def encrypt(self): 
        self.cipherList = []
        for p in self.plainList:
            self.OAEP.setM(p)
            self.OAEP.encode()
            plain = int(self.OAEP.getEM(), 16)
            cipher = modPower(plain, self.e, self.n)
            self.cipherList.append("%0256x"%cipher)
        #print(self.cipherList) 

    def decrypt(self):
        self.plainList = []
        with open("private.txt", "r") as f:
            keys = f.readlines()
        p = int(keys[0].strip())
        q = int(keys[1].strip())
        d = int(keys[2].strip())
        n = p * q
        for c in self.cipherList:
            #print(c)
            cipher = int(c, 16)
            #plain = modPower(cipher, d, self.n)
            r1 = d % (p - 1)
            r2 = d % (q - 1)
            p1 = modPower(cipher, r1, p)
            p2 = modPower(cipher, r2, q)
            plain = CRT([p1, p2], [p, q], n)
            self.OAEP.setEM("%0256x"%plain)
            self.OAEP.decode()
            temp = self.OAEP.getM()
            self.plainList.append([int(temp[i:i+2], 16) for i in range(0, len(temp), 2)])

    def outputCipher(self):
        with open(self.address + ".Encrypted", "wb") as f:
            for c in self.cipherList:
                temp = [int(c[t:t+2], 16) for t in range(0, 256, 2)]
                f.write(bytes(temp))
    
    def outputPlain(self):
        pad = self.plainList[-1]
        padNum = pad[-1] + 1
        #print(padNum)
        #print(self.plainList[-1])
        self.plainList[-1] = self.plainList[-1][:padNum]
        #print(self.plainList[-1])
        with open(self.address[:-10], "wb") as f:
            for p in self.plainList:
                f.write(bytes(p))

if __name__ == '__main__':
    r = RSA("/Users/WangJM/Desktop/前奏曲.jpg.Encoded.log")
    r.setMsg()
    r.encrypt()
    r.outputCipher()
    t = RSA("/Users/WangJM/Desktop/前奏曲.jpg.Encoded.log.Encrypted")
    t.setCip()
    t.decrypt()
    t.outputPlain()
