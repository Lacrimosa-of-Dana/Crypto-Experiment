# -*- coding: utf-8 -*-
# 原根
from time import clock
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

# 计算Euler函数，顺便返回n的素因子用于判断原根存在性
# 利用公式 phi(n) = n(1-1/p1)(1-1/p2)...(1-1/pn)
def phi(n):
	result = n
	i = 2
	while i * i <= n:
		if n % i == 0:
			while n % i == 0:
				n /= i
			result -= result // i
		i += 1
	if n > 1:
		result -= result //n
	return result

# 求原根
def primitive(n):
	if n == 2:
		return [1]
	euler = phi(n)
	roots = []
	temp = euler
	# 对phi(n)进行素因子分解
	factors = []
	i = 2
	while i * i <= temp:
		if temp % i == 0:
			factors.append(i)
			while temp % i == 0:
				temp /= i 
		i += 1
	if temp > 1:
		factors.append(temp)

	# 开始寻找原根
	for g in range(2, n):
		for p in factors:
			if modPower(g, euler / p, n) == 1 or modPower(g, euler, n) != 1:
				break
		else:
			roots.append(g)
	return roots

# 测试用人机接口
def main():
	n = int(input())
	start = clock()
	g = primitive(n)
	end = clock()
	if g == []:
		print("%d does not have a primitive root."%n)
	else:
		print("Primitive roots of %d:"%n)
		print(g)
	print("Runtime is %.5fs."%(end - start))

if __name__ == '__main__':
	main()



