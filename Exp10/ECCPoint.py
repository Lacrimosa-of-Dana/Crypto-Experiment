class ECCPoint(object):
    '''
    p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
    a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
    b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
    n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
    xg = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
    yg = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
    '''
    p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
    a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
    b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
    xg = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
    yg = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
    n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def reverse(target, mod):
        if target < mod:
            change = True
            big, small = mod, target
        else:
            change = False
            big, small = target, mod

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
            return coeSmall if coeSmall >= 0 else coeSmall + mod
        else:
            return coeBig if coeBig >= 0 else coeBig + mod


    def __add__(self, target):
        if (self.x == target.x and self.y == target.y):
            lam = ((3 * self.x * self.x + ECCPoint.a) * self.reverse((2 * self.y) % ECCPoint.p, ECCPoint.p)) %  ECCPoint.p
        else:
            lam = ((target.y - self.y) * self.reverse((target.x - self.x) % ECCPoint.p, ECCPoint.p)) %  ECCPoint.p
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
