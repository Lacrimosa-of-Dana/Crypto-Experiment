import sys
from ECCPoint import *
def int_to_bytes(x, lenk):
    return x.to_bytes(lenk, byteorder='big')

def bytes_to_int(m):
    return int.from_bytes(m, byteorder='big')

def elm_to_bytes(a):
    return int_to_bytes(a, 32)

def bytes_to_elm(s):
    return bytes_to_int(s)

def point_to_bytes(p):
    x1 = elm_to_bytes(p.x)
    y1 = elm_to_bytes(p.y)
    s = b'\x04'
    return b''.join([s, x1, y1])

def bytes_to_point(s):
    p = ECCPoint(bytes_to_int(s[1:33]), bytes_to_int(s[33:]))
    lhs = (p.y * p.y) % ECCPoint.p
    rhs = (p.x * p.x * p.x + ECCPoint.a * p.x * p.x + ECCPoint.b) % ECCPoint.p
    '''
    if lhs != rhs:
        print("Error raised in transferring bytes into point.")
        sys.exit(0)
    '''
    return p 

