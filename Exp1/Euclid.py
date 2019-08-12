
def backEuclid(num1, num2):
	if num1 < num2:
		change = True
		big, small = num2, num1
	else:
		change = False
		big, small = num1, num2
	if small == 0:
		return big, 1, 0
	else:
		rest, coeBig_n, coeSmall_n = backEuclid(small, big % small)
		coeBig = coeSmall_n
		coeSmall = coeBig_n - coeSmall_n * big // small
		if change:
			return rest, coeSmall, coeBig
		else:
			return rest, coeBig, coeSmall

a = int(input())
b = int(input())
if a < b:
    a, b = b, a
r, x, y = backEuclid(a, b)
print(r)
print(x)
print(y)
