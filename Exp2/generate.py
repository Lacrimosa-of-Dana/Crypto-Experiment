# -*- coding: utf-8 -*-

#！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
# WARNING：
# 这个实验的需求描述极其不清晰，我无法理解具体输入什么输出什么
# 询问老师没有得到能让人理解的答案
# 本原多项式的取值来自哪个域也没有说明，导致这个实验毫无意义
# 本算法以整数环为唯一分解环
#！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！

from random import randint
def Euclid(num1, num2):
	# 首先调整大小，保证num1 > num2
	if num1 < num2:
		num1, num2 = num2, num1
	while num1 % num2 != 0:
		num1, num2 = num2, num1 % num2
	return num2

def generate(n):
	factor = []
	# 生成随机数
	factor.append(randint(1, 50))
	gcd = factor[0]
	for i in range(1, n + 1):
		while True:
			temp = randint(1, 50)
			tgcd = Euclid(temp, gcd)
			# 只要互素就继续取下一个
			if tgcd == 1:
				tgcd = gcd
				factor.append(temp)
				break
	return factor

def main():
	n = int(input())
	factors = generate(n)
	print("%d + "%factors[0], end = '')
	for i in range(1, len(factors) - 1):
		print("%dx^%d + "%(factors[i], i), end = '')
	print("%dx^%d"%(factors[n], n))
if __name__ == '__main__':
	main()