# -*- coding: utf-8 -*-
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

def reverse(num, mod):
    rest, coe1, coe2 = extendEuclid(num, mod)
    return coe1

def AffineCipher(message, a, b):
    cipher = []
    for c in message:
        cipher.append(chr((a * (ord(c.upper()) - ord('A')) + b) % 26 + ord('A')))
    return ''.join(cipher)

def AffineDecrypt(cipher, keya, keyb):
    message = []
    for c in cipher:
        temp = (ord(c.upper()) - ord('A') - keyb) % 26
        message.append(chr((temp * keya) % 26 + ord('A')))
    return ''.join(message)

def main():
    print("Input the message:")
    message = input()
    while True:
        a = int(input("Input a: "))
        b = int(input("Input b: "))
        a %= 26
        b %= 26
        if extendEuclid(a, 26)[0] == 1:
            break
        else:
            print("Illegal parameter!")
    print("Encrypt finished. The cipher is:")
    cipher = AffineCipher(message, a, b)
    print(cipher)
    print()
    print("=" * 20)
    print()
    while True:
        keya = int(input("Input keya: "))
        keyb = int(input("Input keyb: "))
        keya %= 26
        keyb %= 26
        print(AffineDecrypt(cipher, keya, keyb))
        if (keya - reverse(a, 26)) % 26 != 0 or (keyb - b) % 26 != 0:
            print("Seem to be the wrong key.")
        else:
            break

if __name__ == '__main__':
    main()
