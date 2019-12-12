import numpy as np
import hashlib
from math import ceil
from time import time
b = 1600
w = 64
l = 6
nr = 24
def string_to_state(S):
    return np.transpose(np.reshape(S, (5, 5, w)), axes=(1, 0, 2))

def state_to_string(A):
    return np.reshape(np.transpose(A, axes=(1, 0, 2)), (b,))

def theta(A):
    C = A[:, 0, :] ^ A[:, 1, :] ^ A[:, 2, :] ^ A[:, 3, :] ^ A[:, 4, :]
    D = np.roll(C, 1, axis=0) ^ np.roll(C, (-1, 1), axis=(0, 1))
    return A ^ np.repeat(D[:, np.newaxis, :], 5, axis=1)

def rho(A):
    A1 = np.zeros((5, 5, w), dtype=int)
    A1[0][0] = A[0][0].copy()
    x, y = 1, 0
    for t in range(24):
        A1[x][y] = np.roll(A[x][y], (t+1)*(t+2)//2)
        x, y = y, (2 * x + 3 * y) % 5
    return A1

def pi(A):
    A1 = np.zeros((5, 5, w), dtype=int)
    for x in range(5):
        for y in range(5):
            A1[x][y] = A[(x+3*y)%5][x].copy()
    return A1

def chi(A):
    return A ^ ((np.roll(A, -1, axis=0) ^ np.ones((5, 5, w), dtype=int)) & np.roll(A, -2, axis=0))

def rc(t):
    if t % 255 == 0:
        return 1
    r = [1, 0, 0, 0, 0, 0, 0, 0]
    for i in range(t % 255):
        r = [0] + r
        r[0] ^= r[8]
        r[4] ^= r[8]
        r[5] ^= r[8]
        r[6] ^= r[8]
        r = r[:8]
    return r[0]

def iota(A, ir):
    A1 = A.copy()
    RC = np.zeros((w, ), dtype=int)
    for j in range(l + 1):
        RC[(1 << j)-1] = rc(j + 7 * ir)
    A1[0][0] ^= RC
    return A1

def Rnd(A, ir):
    return iota(chi(pi(rho(theta(A)))), ir)

def Keccak_p(S):
    A = string_to_state(S)
    for ir in range(12 + 2 * l - nr, 12 + 2 * l):
        A = Rnd(A, ir)
    return state_to_string(A)

def pad(x, m):
    j = (- m - 2) % x
    return np.array([1] + [0] * j + [1])

def sponge(r, N, d):
    P = np.concatenate((N, pad(r, len(N))))
    n = len(P) // r
    c = b - r
    part = []
    for i in range(n):
        part.append(P[i*r:(i+1)*r])
    S = np.zeros((b,), dtype=int)
    zeroc = np.zeros((c, ), dtype=int)
    for i in range(n):
        S = Keccak_p(S ^ np.concatenate((part[i], zeroc)))
    Z = np.array([], dtype=int)
    while True:
        Z = np.concatenate((Z, S[:r]))
        if d <= len(Z):
            return Z[:d]
        S = Keccak_p(S)

def Keccak(c, N, d):
    return sponge(1600 - c, N, d)

def bytes_to_bits(B, n):
    S = np.zeros((8 * len(B), ), dtype=int)
    for i in range(len(B)):
        for j in range(8):
            S[8*i+j] = (B[i] >> j) & 1
    return S[:n]

def bits_to_hex(S):
    n = len(S)
    if -n % 8 != 0:
        T = np.concatenate(S, np.zeros((-n % 8, ), dtype=int))
    else:
        T = S.copy()
    m = ceil(n / 8)
    H = []
    for i in range(m):
        temp = 0
        for j in range(8):
            temp <<= 1
            temp |= T[8*i+7-j]
        H.append('%02X'%temp)
    return ''.join(H)

def SHA3_224(M):
    return bits_to_hex(Keccak(448, np.concatenate((bytes_to_bits(M, 8 * len(M)), np.array([0, 1]))), 224))

def SHA3_256(M):
    return bits_to_hex(Keccak(512, np.concatenate((bytes_to_bits(M, 8 * len(M)), np.array([0, 1]))), 256))

def SHA3_384(M):
    return bits_to_hex(Keccak(768, np.concatenate((bytes_to_bits(M, 8 * len(M)), np.array([0, 1]))), 384))

def SHA3_512(M):
    return bits_to_hex(Keccak(1024, np.concatenate((bytes_to_bits(M, 8 * len(M)), np.array([0, 1]))), 512))


if __name__ == '__main__':
    with open("input.txt", "rb") as f:
        M = f.read()
    start = time()
    print(hashlib.sha3_224(M).hexdigest())
    end = time()
    print(end-start)
    start = time()
    print(SHA3_224(M))
    end = time()
    print(end-start)
    print(SHA3_256(M))
    print(SHA3_384(M))
    print(SHA3_512(M))
    