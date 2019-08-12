import SHA1
import SHA3
import sys
import hmac

class HMAC(object):
    def __init__(self, mode):
        self.key = None
        if mode.upper() == "SHA1":
            self.hashFunc = SHA1.SHA1
            self.L = 20
            self.B = 64
        elif mode.upper() == "SHA3_224":
            self.hashFunc = SHA3.SHA3_224
            self.L = 28
            self.B = 144
        elif mode.upper() == "SHA3_256":
            self.hashFunc = SHA3.SHA3_256
            self.L = 32
            self.B = 136
        elif mode.upper() == "SHA3_384":
            self.hashFunc = SHA3.SHA3_384
            self.L = 48
            self.B = 104
        elif mode.upper() == "SHA3_512":
            self.hashFunc = SHA3.SHA3_512
            self.L = 64
            self.B = 72
        else:
            print("Unknown hash function.")
            sys.exit(0)

    def getKey(self):
        with open("key.txt", "rb") as f:
            self.key = f.read()
        
    def mac(self, text):
        ipad = b'\x36' * self.B
        opad = b'\x5c' * self.B
        if len(self.key) > self.B:
            self.key = int(self.hashFunc(self.key), 16).to_bytes(self.L, byteorder='big')
        if len(self.key) < self.B:
            self.key = self.key.ljust(self.B, b'\x00')
        ip = (int.from_bytes(ipad, byteorder='big') ^ int.from_bytes(self.key, byteorder='big')).to_bytes(self.B, byteorder='big')
        hipad = int(self.hashFunc(b''.join([ip, text])), 16).to_bytes(self.L, byteorder='big')
        op = (int.from_bytes(opad, byteorder='big') ^ int.from_bytes(self.key, byteorder='big')).to_bytes(self.B, byteorder='big')
        return self.hashFunc(b''.join([op, hipad]))

if __name__ == '__main__':
    HMAC_SHA1 = HMAC("SHA1")
    HMAC_SHA1.getKey()
    with open("input.txt", "rb") as f:
        text = f.read()
    print(HMAC_SHA1.mac(text))
    h = hmac.new(HMAC_SHA1.key, text, digestmod='SHA1')
    print(h.hexdigest())
    HMAC_SHA3 = HMAC("SHA3_512")
    HMAC_SHA3.getKey()
    with open("input.txt", "rb") as f:
        text = f.read()
    print(HMAC_SHA3.mac(text))
    h = hmac.new(HMAC_SHA3.key, text, digestmod='sha3_512')
    print(h.hexdigest())


