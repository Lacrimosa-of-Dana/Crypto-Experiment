import hashlib
from random import randint
import sys
class BirthdayAttack(object):
    def __init__(self, mode):
        if mode.upper() == "SHA1":
            self.hashFunc = hashlib.sha1
            self.L = 160
        elif mode.upper() == "SHA3_224":
            self.hashFunc = hashlib.sha3_224
            self.L = 224
        elif mode.upper() == "SHA3_256":
            self.hashFunc = hashlib.sha3_256
            self.L = 256
        elif mode.upper() == "SHA3_384":
            self.hashFunc = hashlib.sha3_384
            self.L = 384
        elif mode.upper() == "SHA3_512":
            self.hashFunc = hashlib.sha3_512
            self.L = 512
        else:
            print("Unknown hash function.")
            sys.exit(0)
        self.birth = {}
        #self.birth2 = {}
        #self.hashSet1 = set()
        #self.hashSet2 = set()

    def attack(self, length):
        for i in range(1 << 40):
            n = randint(0, 1 << self.L).to_bytes(self.L // 8, byteorder='big')
            h = self.hashFunc(n).hexdigest()[:length]
            try:
                self.birth[h]
            except KeyError as e:
                self.birth[h] = n
            else:
                return self.birth[h], n, i
            #self.birth2[h2] = n2
            #self.hashSet1.add(h1)
            #self.hashSet2.add(h2)
            #test = self.hashSet1.intersection(self.hashSet2)
            #if test != set():
            #    pump = test.pop()
            #    return self.birth1[pump], self.birth2[pump]

if __name__ == '__main__':
    a = BirthdayAttack("SHA1")
    pair = a.attack(10)
    print(pair[0])
    print(a.hashFunc(pair[0]).hexdigest())
    print(pair[1])
    print(a.hashFunc(pair[1]).hexdigest())


