from AES import *
from util import *

class CFB(object):
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

    def encrypt(self, mode):
        shiftReg = self.IV
        partEncrypt = AES()
        for p in self.plain:
            partEncrypt.set(shiftReg, self.key)
            partEncrypt.encrypt()
            partCipher = int(partEncrypt.getCipher()[:2], 16) ^ p
            if mode == "ENCRYPT":
                shiftReg = shiftReg[2:] + int_to_hex(partCipher, 2)
            else:
                shiftReg = shiftReg[2:] + int_to_hex(p, 2)
            self.cipher.append(partCipher)

    def output(self, mode):
        if mode == "ENCRYPT":
            with open(self.addr + ".Encrypted", "wb") as cipherFile:
                cipherFile.write(bytes(self.cipher))
        else:
            with open(self.addr[:-10], "wb") as cipherFile:
                cipherFile.write(bytes(self.cipher))

if __name__ == '__main__':
    test = CFB("test.txt", "0f1571c947d9e8590cb7add6af7f6798", "0123456789abcdeffedcba9876543210")
    test.encrypt("ENCRYPT")
    test.output("ENCRYPT")
    dec = CFB("test.txt.Encrypted", "0f1571c947d9e8590cb7add6af7f6798", "0123456789abcdeffedcba9876543210")
    dec.encrypt("DECRYPT")
    dec.output("DECRYPT")
