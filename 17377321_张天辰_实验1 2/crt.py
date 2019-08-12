# -*- coding: utf-8 -*-
from extendEuclid import extendEuclid
import time
# 解中国剩余定理

# 求数论倒数（逆）
# gcd = coeN * n + mod * coeMod
# 两边取模即得coeN为n模mod的数论倒数
def reverse(n, mod):
	gcd, coeN, coeMod = extendEuclid(n, mod)
	return coeN

# remainders是余数列表，mods是模列表，modProduct是模之积
def CRT(remainders, mods, modProduct):
	root = 0
	for i in range(len(mods)):
	    rest = modProduct / mods[i]
	    rev = reverse(rest, mods[i])
	    root += rev * rest * remainders[i]
	    root = root % modProduct
	return root

# 测试用人机接口
def main():
	n = int(input("Input number of formulas: "))
	remainders = []
	mods = []
	modProduct = 1
	for i in range(n):
	    r = int(input("Remainder: "))
	    mod = int(input("Mod:"))
	    remainders.append(r)
	    mods.append(mod)
	    modProduct *= mod
	start = time.clock()
	root = CRT(remainders, mods, modProduct)
	end = time.clock()
	print("x = %d (mod %d)"%(root, modProduct))
	print("Runtime is %.5fs."%(end - start))

if __name__ == '__main__':
	main()


