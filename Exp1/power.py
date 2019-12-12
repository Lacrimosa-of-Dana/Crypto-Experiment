# -*- coding: utf-8 -*-
import time
# 平方乘算法

def badPower(base, power, mod):
    result = 1;
    i = 1;
    while i <= power:
        result = (result * base) % mod
        i += 1
    return result

def modPower(base, power, mod):
    binary = str(bin(power))[2:]
    # 把指数power转化为二进制
    # 这一步得到的字符串应该是"0b....."形式，故应从下标2开始
    result = 1;
    for i in binary:
        if i == '0':
            result = (result * result) % mod
        else:
            result = (result * result) % mod
            result = (result * base) % mod
        print(i)
        print(result)
    return result

# 测试用人机接口
def main():
    base = int(input("base="))
    power = int(input("power="))
    mod = int(input("mod="))
    
    print("BadPower:")
    start = time.clock()
    #result = badPower(base, power, mod)
    end = time.clock()
    #print("The result is %d."%result)
    print("Runtime is %.5fs."%(end - start))
    
    print("GoodPower:")
    start = time.clock()
    result = modPower(base, power, mod)
    end = time.clock()
    print("The result is %d."%result)
    print("Runtime is %.5fs."%(end - start))

if __name__ == '__main__':
    main()
