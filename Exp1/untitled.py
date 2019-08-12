def Euclid(num1, num2):
	if num1 < num2:
		num1, num2 = num2, num1
	while num1 % num2 != 0:
		num1, num2 = num2, num1 % num2
	return num2


print(Euclid(200,105))