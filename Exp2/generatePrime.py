from PrimeTest import *
print("start")
for i in range((1<<1023)+1, (1<<1024)+1, 2):
    if MillerRabin(i, 10) and Fermat(i, 10) and SolovayStassen(i, 10):
        print(i)
