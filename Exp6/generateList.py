from util import *
t0 = []
t1 = []
t2 = []
t3 = []
ReT0 = []
ReT1 = []
ReT2 = []
ReT3 = []
for x in range(1<<8):
    s = S_BOX[x//16][x%16]
    t0.append([int(multiply(int_to_bin(s), "00000010"), 2), 
            int(multiply(int_to_bin(s), "00000001"), 2), 
            int(multiply(int_to_bin(s), "00000001"), 2), 
            int(multiply(int_to_bin(s), "00000011"), 2)])
    t1.append([int(multiply(int_to_bin(s), "00000011"), 2), 
            int(multiply(int_to_bin(s), "00000010"), 2), 
            int(multiply(int_to_bin(s), "00000001"), 2), 
            int(multiply(int_to_bin(s), "00000001"), 2)])
    t2.append([int(multiply(int_to_bin(s), "00000001"), 2), 
            int(multiply(int_to_bin(s), "00000011"), 2), 
            int(multiply(int_to_bin(s), "00000010"), 2), 
            int(multiply(int_to_bin(s), "00000001"), 2)])
    t3.append([int(multiply(int_to_bin(s), "00000001"), 2), 
            int(multiply(int_to_bin(s), "00000001"), 2), 
            int(multiply(int_to_bin(s), "00000011"), 2), 
            int(multiply(int_to_bin(s), "00000010"), 2)])
    s1 = REV_S_BOX[x//16][x%16]
    ReT0.append([int(multiply(int_to_bin(s1), "00001110"), 2), 
            int(multiply(int_to_bin(s1), "00001001"), 2), 
            int(multiply(int_to_bin(s1), "00001101"), 2), 
            int(multiply(int_to_bin(s1), "00001011"), 2)])
    ReT1.append([int(multiply(int_to_bin(s1), "00001011"), 2), 
            int(multiply(int_to_bin(s1), "00001110"), 2), 
            int(multiply(int_to_bin(s1), "00001001"), 2), 
            int(multiply(int_to_bin(s1), "00001101"), 2)])
    ReT2.append([int(multiply(int_to_bin(s1), "00001101"), 2), 
            int(multiply(int_to_bin(s1), "00001011"), 2), 
            int(multiply(int_to_bin(s1), "00001110"), 2), 
            int(multiply(int_to_bin(s1), "00001001"), 2)])
    ReT3.append([int(multiply(int_to_bin(s1), "00001001"), 2), 
            int(multiply(int_to_bin(s1), "00001101"), 2), 
            int(multiply(int_to_bin(s1), "00001011"), 2), 
            int(multiply(int_to_bin(s1), "00001110"), 2)])
print(t0)
print('')
print(t1)
print('')
print(t2)
print('')
print(t3)
print('')
print('=' * 20)
print('')
print(ReT0)
print('')
print(ReT1)
print('')
print(ReT2)
print('')
print(ReT3)
