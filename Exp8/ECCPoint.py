class ECCPoint(object):
    p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
    a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
    b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
    n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
    xg = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
    yg = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def reverse(target):
        if target < ECCPoint.p:
            change = True
            big, small = ECCPoint.p, target
        else:
            change = False
            big, small = target, ECCPoint.p

        # 根据算法进行计算，所有名字后带 _n 的变量相当于原变量下标 + 1
        rest, coeBig, coeSmall = big, 1, 0
        rest_n, coeBig_n, coeSmall_n = small, 0, 1
        while rest_n != 0:
            q = rest // rest_n
            temp1 = rest - q * rest_n
            temp2 = coeBig - q * coeBig_n
            temp3 = coeSmall - q * coeSmall_n
            rest, coeBig, coeSmall = rest_n, coeBig_n, coeSmall_n
            rest_n, coeBig_n, coeSmall_n = temp1, temp2, temp3

        # 如果因为大小关系交换了输入的两个参数的顺序，在这里要换回来
        if change:
            return coeSmall if coeSmall >= 0 else coeSmall + ECCPoint.p
        else:
            return coeBig if coeBig >= 0 else coeBig + ECCPoint.p


    def __add__(self, target):
        if (self.x == target.x and self.y == target.y):
            lam = ((3 * self.x * self.x + ECCPoint.a) * self.reverse((2 * self.y) % ECCPoint.p)) %  ECCPoint.p
        else:
            lam = ((target.y - self.y) * self.reverse((target.x - self.x) % ECCPoint.p)) %  ECCPoint.p
        x = (lam * lam - self.x - target.x) % ECCPoint.p
        y = (lam * (self.x - x) - self.y) % ECCPoint.p
        return ECCPoint(x, y)

    def __sub__(self, target):
        return self + ECCPoint(target.x, ECCPoint.p - target.y)

    def multi(self, time):
        b = bin(time)[3:]
        result = ECCPoint(self.x, self.y)
        for i in b:
            if i == '1':
                result = result + result
                result = result + self
            else:
                result = result + result
        return result

    def outputPosition(self):
        return (self.x, self.y)

if __name__ == '__main__':
    a = ECCPoint(16, 5)
    b = ECCPoint(14, 14)
    c = ECCPoint(20, 20)
    print((a+a).outputPosition())
    print((a+c).outputPosition())
    print((c+a).outputPosition())
    print(a.multi(3).outputPosition())
    print(b.multi(3).outputPosition())
