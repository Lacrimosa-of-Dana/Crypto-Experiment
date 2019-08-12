from AES import *
from util import *
from copy import deepcopy
import sys
class CBC(object):
    def __init__(self, addr, src_key, initVector):
        self.addr = addr
        self.file = None
        self.plain = None
        with open(addr, "rb") as self.file:
            self.plain = self.file.read()
        self.key = Key(src_key)
        self.key.generateKey()
        self.IV = initVector
        self.cipher = []

    def encrypt(self):
        initV = deepcopy(self.IV)
        #initVector = [int(initV[i:i+2], 16) for i in range(0, 32, 2)]
        length = len(self.plain)
        self.plain = list(self.plain)
        mod = length % 16
        if mod == 0:
            self.plain.extend([16] * 16)
            length += 16
        else:
            self.plain.extend([16 - mod] * (16 - mod))
            length += 16 - mod
        partEncrypt = AES()
        for i in range(0, length, 16):
            initVector = [int(initV[i:i+2], 16) for i in range(0, 32, 2)]
            partList = [self.plain[i+j] ^ initVector[j] for j in range(16)]
            partPlain = ''.join([int_to_hex(partList[j], 2) for j in range(16)])
            partEncrypt.set(partPlain, self.key)
            partEncrypt.encrypt()
            self.cipher.append(partEncrypt.getCipher())
            initV = deepcopy(partEncrypt.getCipher())

    def decrypt(self):
        initVector = deepcopy(self.IV)
        partDecrypt = AES()
        for i in range(0, len(self.plain), 16):
            partPlain = ''.join([int_to_hex(self.plain[i+j], 2) for j in range(16)])
            partDecrypt.set(partPlain, self.key)
            partDecrypt.decrypt()
            partCipher = int_to_hex(int(partDecrypt.getCipher(), 16) ^ int(initVector, 16), 32)
            self.cipher.append(partCipher)
            initVector = deepcopy(partPlain)
        print(self.cipher[-1])
        paddle = int(self.cipher[-1][-2:], 16)
        print(paddle)
        self.cipher[-1] = self.cipher[-1][:-2*paddle]
        print(self.cipher[-1])

    def output(self, mode):
        if mode == "ENCRYPT":
            with open(self.addr + ".Encrypted", "wb") as cipherFile:
                for c in self.cipher:
                    cipherFile.write(bytes(str_to_8bitList(c)))
        else:
            with open(self.addr[:-10], "wb") as cipherFile:
                for c in self.cipher:
                    if c != '':
                        cipherFile.write(bytes(str_to_8bitList(c)))

