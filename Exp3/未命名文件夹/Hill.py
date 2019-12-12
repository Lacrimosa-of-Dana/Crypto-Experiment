import numpy as np
import numpy.linalg
global format_num
def det(m):
        # 有好的工具却弃之不用，等于是自废武功。 ----单墫
        return int(round(numpy.linalg.det(m))) % 2
# 生成矩阵
def generate(size):
        while True:
                print("Input key(in binary):")
                m = []
                for i in range(size):
                        temp = input().split()
                        temp = [int(n) for n in temp]
                        m.append(temp)
                m = np.matrix(m)
                if det(m) != 0:
                        break
                else:
                        print("Matrix illegal.")
        return m

# 矩阵求逆，用高斯消元法
def rev(a, n):
    rmax = []
    cmax = []
    max_t = 0
    for k in range(n):
        max_t = 0
        for i in range(k, n):
            for j in range(k, n):
                if a[i][j] > max_t:
                    max_t = a[i][j]
                    rmax.append(i)
                    cmax.append(j)
                    
        if max_t == 0:
            print("Matrix illegal.")
            return 

        if rmax[k] != k:
            for j in range(n):
                a[k][j], a[rmax[k]][j] = a[rmax[k]][j], a[k][j]
        if cmax[k] != k:
            for i in range(n):
                a[i][k], a[i][cmax[k]] = a[i][cmax[k]], a[i][k]

        for j in range(n):
            if j != k:
                a[k][j] = a[k][j] * a[k][k]
        for i in range(n):
            if i != k:
                for j in range(n):
                    if j != k:
                        a[i][j] = a[i][j] ^ (a[i][k]*a[k][j])
        for i in range(n):
            if i != k:
                a[i][k]=a[i][k]*a[k][k]

    for k in range(n - 1, -1, -1):
        if cmax[k] != k:
            for j in range(n):
                a[k][j], a[cmax[k]][j] = a[cmax[k]][j], a[k][j]
            if rmax[k] != k:
                for i in range(n):
                    a[i][k], a[i][rmax[k]] = a[i][rmax[k]], a[i][k]


    
# 矩阵乘向量
def mul(key, mes, size):
        rst = []
        for i in range(size):
                temp = 0
                for j in range(size):
                        temp += key.tolist()[i][j] * mes[j]
                        temp %= 2
                rst.append(temp)
        return rst

# 加密
def HillEncrypt(key, message, size):
        global format_num
        tempm = [('{:0' + str(format_num) + 'b}').format(ord(c)) for c in message]
        intm = []
        for t in tempm:
                for bit in t:
                        intm.append(int(bit))
        cipher = []
        for i in range(0, len(intm), size):
                cipher.extend(mul(key, intm[i:i+size], size))
        return ''.join(str(c) for c in cipher)

# 解密，和加密差不多
def HillDecrypt(key, cipher, size):
        global format_num
        intc = [int(t) for t in cipher]
        message = []
        msgt = []
        key_1 = key.tolist()
        rev(key_1, size)
        key_1 = np.matrix(key_1)
        for i in range(0, len(intc), size):
                msgt.extend(mul(key_1, intc[i:i+size], size))
        msgt = ''.join([str(c) for c in msgt])
        message = [chr(int(msgt[i:i+format_num], 2))
                   for i in range(0, len(msgt), format_num)]    
        return ''.join(message)

def HillPwn(message, cipher, size):
        global format_num
        tempm = [('{:0' + str(format_num) + 'b}').format(ord(c)) for c in message]
        intm = []
        for t in tempm:
                for bit in t:
                        intm.append(int(bit))
        intc = [int(t) for t in cipher]
        if len(intc) < size ** 2:
                print("Not long enough. Failed.")
                return
        
        flag = 0
        while True:
                m_mat = []
                c_mat = []
                for i in range(size):
                        temp1 = []
                        temp2 = []
                        for j in range(size):
                                if flag >= len(intc):
                                        print("Failed.")
                                        return
                                temp1.append(intm[flag])
                                temp2.append(intc[flag])
                                flag += 1
                        m_mat.append(temp1)
                        c_mat.append(temp2)
                m_mat = np.matrix(m_mat).T
                c_mat = np.matrix(c_mat).T
                if det(m_mat) != 0:
                        break
        else:
                print("Failed.")
                return
        m1 = m_mat.tolist()
        rev(m1, size)
        m_mat = np.matrix(m1)
        m_temp = np.dot(c_mat, m_mat)
        key_rst = m_temp.tolist()
        for i in range(size):
                for j in range(size):
                        key_rst[i][j] %= 2
                        print(key_rst[i][j], end=' ')
                print('')


def main():
        global format_num
        lan = int(input("You are encrypting Chinese(input 1) or English(input 2) ?"))
        if lan == 1:
                format_num = 16
        else:
                format_num = 8
        size = int(input("Input size of matrix: "))
        key = generate(size)
        print("Input message: ")
        message = input()
        cipher = HillEncrypt(key, message, size)
        print(hex(int(cipher, 2))[2:])
        print('='*20)
        while True:
                keyd = generate(size)
                mes = HillDecrypt(keyd, cipher, size)
                print(mes)
                if keyd.tolist() == key.tolist():
                        break
                else:
                        print("Seem to be the wrong key.")
        HillPwn(message, cipher, size)
if __name__ == '__main__':
        main()
