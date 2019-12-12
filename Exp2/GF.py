# -*- coding: utf-8 -*-
# Galois Field(256)
# x^8 +x^4 + x^3 + x +1
# 生成元为x + 1

# 加法就是异或
def add(elm1, elm2):
	num1 = int(elm1, 2)
	num2 = int(elm2, 2)
	return '{:08b}'.format(num1 ^ num2)
# 减法同加法
def sub(elm1, elm2):
	return add(elm1, elm2)

# 一种移位乘法
def multiply(elm1, elm2):
	elm2 = elm2[: : -1]
	result = 0
	temp = int(elm1, 2)
	for i in range(8):
		if elm2[i] == '1':
			result ^= temp
		str_temp = '{:08b}'.format(temp)
		# 取模
		if str_temp[0] == '1':
			temp = int(str_temp[1: ] + '0', 2) ^ int("0x1B", 16)
		else:
			temp = int(str_temp[1: ] + '0', 2)
	return '{:08b}'.format(result)

# 打表
multi = [0] * 256
multi[0] = 1
# 生成元表
for i in range(1, 255):
	multi[i] = (multi[i - 1] << 1) ^ multi[i - 1]
	if multi[i] & 0x100:
		multi[i] ^= 0x11B
# 生成元反表
arc_multi = [0] * 256
for i in range(255):
	arc_multi[multi[i]] = i
# 逆表
reverse = [0] * 256
for i in range(1, 256):
	reverse[i] = multi[(255 - arc_multi[i]) % 255]

# 打表求解乘除和逆
def table_multiply(elm1, elm2):
	return '{:08b}'.format(
		multi[(arc_multi[int(elm1, 2)] + arc_multi[int(elm2, 2)]) % 255])
def table_rev(elm):
	return '{:08b}'.format(reverse[int(elm, 2)])
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
        for i in range(1, 1<<8):
                for j in range(1, 1<<8):
                        if multiply('{:08b}'.format(i), '{:08b}'.format(j)) != table_multiply('{:08b}'.format(i), '{:08b}'.format(j)):
                                print([i, j])
        main()
