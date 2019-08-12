from random import randint
from ECCPoint import *
from util import *
import hashlib
from gmssl import sm3, sm2

class SM2Sign(object):
    g = ECCPoint(ECCPoint.xg, ECCPoint.yg)

    def __init__(self, id):
        self.id = id.encode('utf-8');
        self.entl = int_to_bytes(len(id) * 8, 2)
        self.private = None
        self.public = None

    def generateKey(self):
        #self.private = randint(3, ECCPoint.n - 1)
        self.private = 0x128B2FA8BD433C6C068C8D803DFF79792A519A55171B1B650C23661D15897263
        self.public = self.g.multi(self.private)

    def sign(self, message):
        '''
        za = hashlib.sha256(b''.join(
            [self.entl, self.id, int_to_bytes(ECCPoint.a, 32), int_to_bytes(ECCPoint.b, 32), 
            int_to_bytes(ECCPoint.xg, 32), int_to_bytes(ECCPoint.yg, 32), 
            int_to_bytes(self.public.x, 32), int_to_bytes(self.public.y, 32)])).digest()
            '''
        za = sm3.sm3_hash(list(b''.join(
            [self.entl, self.id, int_to_bytes(ECCPoint.a, 32), int_to_bytes(ECCPoint.b, 32), 
            int_to_bytes(ECCPoint.xg, 32), int_to_bytes(ECCPoint.yg, 32), 
            int_to_bytes(self.public.x, 32), int_to_bytes(self.public.y, 32)])))
        za = int_to_bytes(int(za, 16), 32)
        m1 = b''.join([za, message])
        #e = bytes_to_int(hashlib.sha256(m1).digest())
        e = int(sm3.sm3_hash(list(m1)), 16)
        while True:
            #k = randint(1, ECCPoint.n - 1)
            k = 0x6CB28D99385C175C94F94E934817663FC176D925DD72B727260DBAAE1FB2F96F
            temp = self.g.multi(k)
            r = (e + temp.x) % ECCPoint.n
            if r == 0 or r + k == ECCPoint.n:
                continue
            s = (ECCPoint.reverse(1 + self.private, ECCPoint.n) * (k - r * self.private)) % ECCPoint.n
            if s != 0:
                break
        return (int_to_bytes(r, 32), int_to_bytes(s, 32))

    def authenticate(self, message, signature):
        r = bytes_to_int(signature[0])
        s = bytes_to_int(signature[1])
        if r < 1 or r >= ECCPoint.n or s < 1 or s >= ECCPoint.n:
            print("Authentication failed.")
            return 0
        '''
        za = hashlib.sha256(b''.join(
            [self.entl, self.id, int_to_bytes(ECCPoint.a, 32), int_to_bytes(ECCPoint.b, 32), 
            int_to_bytes(ECCPoint.xg, 32), int_to_bytes(ECCPoint.yg, 32), 
            int_to_bytes(self.public.x, 32), int_to_bytes(self.public.y, 32)])).digest()
            '''
        za = sm3.sm3_hash(list(b''.join(
            [self.entl, self.id, int_to_bytes(ECCPoint.a, 32), int_to_bytes(ECCPoint.b, 32), 
            int_to_bytes(ECCPoint.xg, 32), int_to_bytes(ECCPoint.yg, 32), 
            int_to_bytes(self.public.x, 32), int_to_bytes(self.public.y, 32)])))
        za = int_to_bytes(int(za, 16), 32)
        m1 = b''.join([za, message])
        #e = bytes_to_int(hashlib.sha256(m1).digest())
        e = int(sm3.sm3_hash(list(m1)), 16)
        t = (r + s) % ECCPoint.n
        if t == 0:
            print("Authentication failed.")
            return 0
        temp = self.g.multi(s) + self.public.multi(t)
        R = (e + temp.x) % ECCPoint.n
        if R == r:
            #print("Authentication passed.")
            return 1
        else:
            #print("Authentication failed.")
            return 0

if __name__ == '__main__':
    
    sign = SM2Sign("ALICE123@YAHOO.COM")
    message = b'message digest'
    sign.generateKey()
    signature = sign.sign(message)
    print(signature)
    sign.authenticate(message, signature)
    sign.authenticate(message, (b'test', b'test'))
