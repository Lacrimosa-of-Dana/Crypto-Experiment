# -*- coding: utf-8 -*-
import time
from math import *
# Euler 筛法

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
			if i % p == 0:
				break
	return primes

def main():
	n = int(input())
	start = time.clock()
	primes = Euler(n)
	end = time.clock()
	print(primes)
	print("Runtime is %.5fs."%(end - start))

if __name__ == '__main__':
	main()
