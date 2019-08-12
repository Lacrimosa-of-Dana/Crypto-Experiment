# -*- coding: utf-8 -*-
import time
from math import *
# Eratosthenes 筛法

def badEratosthenes(n):
	# 10以内素数。作为递归终点
	standard = [2, 3, 5, 7]
	if n < 10:
		return [p for p in standard if p <= n]
	else:
		# 递归根号n以内
		primes = badEratosthenes(int(n ** 0.5))
		flag = [False for i in range(n + 1)]
		for p in primes:
			j = 2 * p
			while j <= n:
				flag[j] = True
				j += p
		return [p for p in range(2, n + 1) if flag[p] == False]

def Eratosthenes(n):
	flag = [False for i in range(n + 1)]
	for i in range(2, int(sqrt(n)) + 1):
		if flag[i] == False:
			# 可以直接从i * i开始算。之前的i的倍数一定已经被筛去
			j = i * i
			while j <= n:
				flag[j] = True
				j += i

	return [p for p in range(2, n + 1) if flag[p] == False]

def Euler(n):
	primes = []
	flag = [True for i in range(n + 1)]
	for i in range(2, n + 1):
		if flag[i]:
			primes.append(i)

		for p in primes:
			if i * p > n:
				break
			flag[i * p] = False
			# 此步原因具体见实验报告
			if i % p == 0:
				break
	return primes

def main():
	n = int(input())
	start = time.clock()
	primes = badEratosthenes(n)
	end = time.clock()
	print("Bad Eratosthenes:")
	print(primes)
	print("Runtime is %.5fs."%(end - start))

	start = time.clock()
	primes = Eratosthenes(n)
	end = time.clock()
	print("Eratosthenes:")
	print(primes)
	print("Runtime is %.5fs."%(end - start))

	start = time.clock()
	primes = Euler(n)
	end = time.clock()
	print("Euler:")
	print(primes)
	print("Runtime is %.5fs."%(end - start))

if __name__ == '__main__':
	main()
