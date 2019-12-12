from random import randint
from math import ceil
import hashlib

def MGF(mgfSeed, maskLen):
    T = ""
    hLen = 256
    for counter in range(ceil(maskLen / hLen)):
        c = mgfSeed + "%08x"%counter
        T += hashlib.sha256(c.encode("utf-8")).hexdigest()
    return T[:2*maskLen]

def generatePrime():
    while True:
        temp = randint((1<<510) + (1<<509), 1<<511)
        p = (temp << 1) + 1
        if (MillerRabin(p)):
            return p

def generateED(phi):
    while True:
        e = randint(3, phi - 1)
        temp = extendEuclid(phi, e)
        if temp[0] == 1:
            return (e, temp[2])

def extendEuclid(num1, num2):
    # 首先保证num1不小于num2
    if num1 < num2:
        change = True
        big, small = num2, num1
    else:
        change = False
        big, small = num1, num2

    # 根据算法进行计算，所有名字后带 _n 的变量相当于原变量下标 + 1
    rest, coeBig, coeSmall = big, 1, 0
    rest_n, coeBig_n, coeSmall_n = small, 0, 1
    while rest_n != 0:
        q = rest // rest_n
        temp1 = rest - q * rest_n
        temp2 = coeBig - q * coeBig_n
        temp3 = coeSmall - q * coeSmall_n
        rest, coeBig, coeSmall = rest_n, coeBig_n, coeSmall_n
        rest_n, coeBig_n, coeSmall_n = temp1, temp2, temp3

    # 如果因为大小关系交换了输入的两个参数的顺序，在这里要换回来
    if change:
        return rest, coeSmall, coeBig
    else:
        return rest, coeBig, coeSmall

def modPower(base, power, mod):
    binary = str(bin(power))[2:]
    # 把指数power转化为二进制
    # 这一步得到的字符串应该是"0b....."形式，故应从下标2开始
    result = 1;
    for i in binary:
        if i == '0':
            result = (result * result) % mod
        else:
            result = (result * result) % mod
            result = (result * base) % mod
    return result

def MillerRabin(n):
    # 先把n表示成2 ^ power * rest的形式
    power = 0
    rest = n - 1
    while not rest & 1:
        rest >>= 1
        power += 1
    for i in range(24):
        rand = randint(2, n - 2)
        if modPower(rand, rest, n) in [1, n - 1]:
            continue
        actPower = rest
        for j in range(power - 1):
            actPower = actPower * 2
            if modPower(rand, actPower, n) == n - 1:
                break
        else:
            return False
    return True

def reverse(n, mod):
    gcd, coeN, coeMod = extendEuclid(n, mod)
    return coeN

# remainders是余数列表，mods是模列表，modProduct是模之积
def CRT(remainders, mods, modProduct):
    root = 0
    for i in range(len(mods)):
        rest = modProduct // mods[i]
        rev = reverse(rest, mods[i])
        root += rev * rest * remainders[i]
        root = root % modProduct
    return root