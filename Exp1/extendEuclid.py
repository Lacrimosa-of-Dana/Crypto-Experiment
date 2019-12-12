# -*- coding: utf-8 -*-
import time
# Euclid算法

def Euclid(num1, num2):
	# 首先调整大小，保证num1 > num2
	if num1 < num2:
		num1, num2 = num2, num1
	while num1 % num2 != 0:
		num1, num2 = num2, num1 % num2
	return num2

def backEuclid(num1, num2):
	# 回溯算法，在除法进行结束之后返回计算系数
	# 先调整大小
	if num1 < num2:
		change = True
		big, small = num2, num1
	else:
		change = False
		big, small = num1, num2

	# 递归终点
	if small == 0:
		return big, 1, 0
	else:
		# 递归
		rest, coeBig_n, coeSmall_n = backEuclid(small, big % small)
		# 回溯计算系数
		coeBig = coeSmall_n
		coeSmall = coeBig_n - coeSmall_n * big // small
		# 如果因为大小关系交换了输入的两个参数的顺序，在这里要换回来
		if change:
			return rest, coeSmall, coeBig
		else:
			return rest, coeBig, coeSmall

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


# 测试用人机接口
def main():
	num1 = int(input("Input num1: "))
	num2 = int(input("Input num2: "))

	print("Euclid:")
	start = time.clock()
	gcd = Euclid(num1, num2)
	end = time.clock()
	print("gcd(%d, %d) = %d"%(num1, num2, gcd))
	print("Runtime is %.5fs."%(end - start))

	print("Back Trace Euclid:")
	start = time.clock()
	gcd, coe1, coe2 = backEuclid(num1, num2)
	end = time.clock()
	print("%d * %d + %d * %d = gcd(%d, %d) = %d"
			%(num1, coe1, num2, coe2, num1, num2, gcd))
	print("Runtime is %.5fs."%(end - start))

	print("Extend Euclid:")
	start = time.clock()
	gcd, coe1, coe2 = extendEuclid(num1, num2)
	end = time.clock()
	print("%d * %d + %d * %d = gcd(%d, %d) = %d"
			%(num1, coe1, num2, coe2, num1, num2, gcd))
	print("Runtime is %.5fs."%(end - start))

if __name__ == '__main__':
	main()
