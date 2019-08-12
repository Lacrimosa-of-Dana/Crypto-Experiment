# -*- coding: utf-8 -*-
# Galois Field(16)
# x^4 + x^3 + 1
# 生成元为x^2
def add(elm1, elm2):
	num1 = int(elm1, 2)
	num2 = int(elm2, 2)
	return '{:04b}'.format(num1 ^ num2)
def sub(elm1, elm2):
	return add(elm1, elm2)

def multiply(elm1, elm2):
	elm2 = elm2[: : -1]
	result = 0
	temp = int(elm1, 2)
	for i in range(4):
		if elm2[i] == '1':
			result ^= temp
		str_temp = '{:04b}'.format(temp)
		if str_temp[0] == '1':
			temp = int(str_temp[1: ] + '0', 2) ^ int("0x9", 16)
		else:
			temp = int(str_temp[1: ] + '0', 2)
	return '{:04b}'.format(result)
# 打表
multi = [0] * 16
multi[0] = 1
# 生成元表
for i in range(1, 15):
	multi[i] = multi[i - 1] << 1
	if multi[i] & 0x10:
		multi[i] ^= 0x19
	multi[i] <<= 1
	if multi[i] & 0x10:
		multi[i] ^= 0x19
# 生成元反表
arc_multi = [0] * 16
for i in range(15):
	arc_multi[multi[i]] = i
# 逆表
reverse = [0] * 16
for i in range(1, 16):
	reverse[i] = multi[(15 - arc_multi[i]) % 15]

# 打表求解乘除和逆
def table_multiply(elm1, elm2):
	return '{:04b}'.format(
		multi[(arc_multi[int(elm1, 2)] + arc_multi[int(elm2, 2)]) % 15])
def table_rev(elm):
	return '{:04b}'.format(reverse[int(elm, 2)])
def divide(elm1, elm2):
	return table_multiply(elm1, table_rev(elm2))       


def main():
	num1 = input()
	num2 = input()
        
	print(num1, "+", num2, "=", add(num1, num2))
	print(num1, "*", num2, "=", multiply(num1, num2))
	print(num1, "*", num2, "=", table_multiply(num1, num2))
	print(num1, "/", num2, "=", divide(num1, num2))
	print(num1, "^ -1 =", table_rev(num1))
	print(num2, "^ -1 =", table_rev(num2))

if __name__ == '__main__':
	main()

