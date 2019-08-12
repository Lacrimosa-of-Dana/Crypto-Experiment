# -*- coding: utf-8 -*-
# 三种素性检验算法
from random import randint
from time import clock

def Euclid(num1, num2):
	# 首先调整大小，保证num1 > num2
	if num1 < num2:
		num1, num2 = num2, num1
	while num1 % num2 != 0:
		num1, num2 = num2, num1 % num2
	return num2

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

# 求Jacobi符号
def Jacobi(a, b):
	result = 1
	a = a % b
	# 特殊情况
	if b == 1:
		return result

	# 如果a = 0则说明已经到了迭代终点
	while a != 0:
		# 首先提取因子2，关于2的Jacobi符号可以直接计算
		while a % 2 == 0:
			a >>= 1
			if b % 8 == 3 or b % 8 == 5:
				result = -result
		# 使用二次互反律
		a, b = b, a	
		if a % 4 == 3 and b % 4 == 3:
			result = - result
		a = a % b
	return result

def MillerRabin(n, times):
	# 先把n表示成2 ^ power * rest的形式
	power = 0
	rest = n - 1
	while not rest & 1:
		rest >>= 1
		power += 1
	for i in range(times):
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

def Fermat(n, times):
	for i in range(times):
		base = randint(1, n - 1)
		gcd = Euclid(n, base)
		if gcd > 1:
			return False
		if modPower(base, n - 1, n) != 1:
			return False
	return True

def SolovayStassen(n, times):
	for i in range(times):
		base = randint(2, n - 2)
		test1 = modPower(base, (n - 1) >> 1, n)
		if test1 == n - 1:
			test1 = -1
		if test1 not in [1, -1]:
			return False
		test2 = Jacobi(base, n)
		if test1 != test2:
			return False
	return True

# 测试用人机接口
def main():
	n = int(input("Input the number to be tested: "))
	times = int(input("Input the test times: "))
	print("MillerRabin:")
	start = clock()
	print(MillerRabin(n, times))
	end = clock()
	print("Runtime is %.5fs."%(end - start))
	print("Fermat:")
	start = clock()
	print(Fermat(n, times))
	end = clock()
	print("Runtime is %.5fs."%(end - start))
	print("SolovayStassen:")
	start = clock()
	print(SolovayStassen(n, times))
	end = clock()
	print("Runtime is %.5fs."%(end - start))

if __name__ == '__main__':
	main()

