import hashlib
from time import time
from numba import jit
#为了加速，使用了jit装饰器。如果没有运行环境，可以将第3行和第11行注释掉
class Sha1(object):
    def __init__(self):
        self.w = None
        self.CV = None
    
    @staticmethod
    @jit
    def lshift(n, k):
        return (n >> (32 - k)) + ((n & ((1 << (32 - k)) - 1)) << k)

    def initLink(self):
        A = 0x67452301
        B = 0xEFCDAB89
        C = 0x98BADCFE
        D = 0x10325476
        E = 0xC3D2E1F0
        self.CV = [A, B, C, D, E]

    #good
    def setBlock(self, plain512):
        self.w = [0] * 80
        for i in range(16):
            self.w[i] = int.from_bytes(plain512[i*4:(i+1)*4], byteorder='big')
        for i in range(16, 80):
            self.w[i] = self.lshift(self.w[i - 3] ^ self.w[i - 8] 
                ^ self.w[i - 14] ^ self.w[i - 16], 1)

    def encode(self):
        A = self.CV[0]
        B = self.CV[1]
        C = self.CV[2]
        D = self.CV[3]
        E = self.CV[4]
        for round in range(20):
            temp = (self.lshift(A, 5) + 
                ((B & C) | ((B ^ 0xffffffff) & D)) + 
                E + self.w[round] + 0x5A827999) & 0xffffffff
            E = D
            D = C
            C = self.lshift(B, 30)
            B = A
            A = temp
        for round in range(20, 40):
            temp = (self.lshift(A, 5) + 
                (B ^ C ^ D) + 
                E + self.w[round] + 0x6ED9EBA1) & 0xffffffff
            E = D
            D = C
            C = self.lshift(B, 30)
            B = A
            A = temp
        for round in range(40, 60):
            temp = (self.lshift(A, 5) + 
                ((B & C) | (B & D) | (C & D)) + 
                E + self.w[round] + 0x8F1BBCDC) & 0xffffffff
            E = D
            D = C
            C = self.lshift(B, 30)
            B = A
            A = temp
        for round in range(60, 80):
            temp = (self.lshift(A, 5) + 
                (B ^ C ^ D) + 
                E + self.w[round] + 0xCA62C1D6) & 0xffffffff
            E = D
            D = C
            C = self.lshift(B, 30)
            B = A
            A = temp
        self.CV[0] = (self.CV[0] + A) & 0xffffffff
        self.CV[1] = (self.CV[1] + B) & 0xffffffff
        self.CV[2] = (self.CV[2] + C) & 0xffffffff
        self.CV[3] = (self.CV[3] + D) & 0xffffffff
        self.CV[4] = (self.CV[4] + E) & 0xffffffff

    def trigger(self, plain):
        self.initLink()
        length = len(plain)
        flag = 0
        while length - flag >= 64:
            self.setBlock(plain[flag:flag+64])
            self.encode()
            flag += 64
        padNum = (64 - 9 - length + flag) % 64
        pad = bytes([128] + [0] * padNum)
        pad = b''.join([pad, (length * 8).to_bytes(8, byteorder='big')])
        rest = b''.join([plain[flag:], pad])
        if len(rest) > 64:
            self.setBlock(rest[:64])
            self.encode()
            rest = rest[64:]
        self.setBlock(rest)
        self.encode()
        return ''.join(["%08X"%c for c in self.CV])
'''   
    def output(self):
        return ''.join(["%08X"%c for c in self.CV])
'''

def SHA1(src):
    return Sha1().trigger(src)

if __name__ == '__main__':
    with open("input.txt", "rb") as f:
        src = f.read()
    start = time()
    print(hashlib.sha1(src).hexdigest())
    end = time()
    print("Runtime is " + str(end - start) + "s")
    start = time()
    print(SHA1(src))
    end = time()
    print("Runtime is " + str(end - start) + "s")
