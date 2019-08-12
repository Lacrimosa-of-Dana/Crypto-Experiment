# -*- coding: utf-8 -*-
import time
from random import randint

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

def MillerRabinTest(n):
	test = n - 1
	power2 = 0
	while not test & 1:
		power2 += 1
		test >>= 1
	for i in range(10):
		base = randint(2, n - 1)
		fund = modPower(base, test, n)
		if fund == 1:
			prime = True
			continue
		for j in range(power2):
			if fund % n == n - 1:
				prime = True
				break
			else:
				fund = (fund * fund) % n
		else:
			return False
	return True

def main():
	n = int(input())
	if MillerRabinTest(n):
		print("prime")
	else:
		print("no")
if __name__ == '__main__':
	main()
