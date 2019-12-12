import sys
# for encrypting
E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]
P_1 = [9, 17, 23, 31, 13, 28, 2, 18, 24, 16, 30, 6, 26, 20, 10, 1, 8, 14, 25, 3, 4, 29, 11, 19, 32, 12, 22, 7, 5, 27, 15, 21]
S1 = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7, 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8, 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0, 15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
S2 = [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10, 3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5, 0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15, 13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
S3 = [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8, 13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1, 13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7, 1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
S4 = [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15, 13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9, 10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4, 3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
S5 = [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9, 14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6, 4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14, 11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
S6 = [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11, 10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8, 9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6, 4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
S7 = [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1, 13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6, 1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2, 6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
S8 = [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7, 1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2, 7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8, 2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
SBOX = [S1, S2, S3, S4, S5, S6, S7, S8]
# for key generating
PC1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
PC2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
PC2_1 = [5, 24, 7, 16, 6, 10, 20, 18, 20, 12, 3, 15, 23, 1, 9, 19, 2, 19, 14, 22, 11, 22, 13, 4, 13, 17, 21, 8, 47, 31, 27, 48, 35, 41, 0, 46, 28, 0, 39, 32, 25, 44, 25, 37, 34, 43, 29, 36, 38, 45, 33, 26, 42, 26, 30, 40]
LShift = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def cycle_Lshift(string, n):
    return string[n:] + string[0:n]

def cycle_Rshift(string, n):
    for i in range(n):
        string = string[-1] + string[0:-1]
    return string

def f(right, key):
    after_e = int(''.join([right[index - 1] for index in E]), 2)
    # print(['{:048b}'.format(after_e)[i:i+6] for i in range(0, 48, 6)])
    # print(['{:048b}'.format(key)[i:i+6] for i in range(0, 48, 6)])
    src_b = '{:048b}'.format(after_e ^ key)
    b = [src_b[i:i + 6] for i in range(0, 48, 6)]
    # print(b)
    after_s = ''.join(['{:04b}'.format(SBOX[i][16 * int(b[i][0] + b[i][-1], 2) + int(b[i][1:-1], 2)]) 
        for i in range(8)])
    # print(after_s)
    result = int(''.join([after_s[index - 1] for index in P]), 2)
    # print("~"*5)
    return result

def s_box(b, i):
    b = '{:06b}'.format(b)
    return '{:04b}'.format(SBOX[i][16 * int(b[0] + b[-1], 2) + int(b[1:-1], 2)]) 

class Message_Cipher_Pair(object):
    __key = "0123456789abcdef"
    __rounds = 3
    def __init__(self, message):
        self.message = message
        self.bin_message = '{:064b}'.format(int(self.message, 16))
        self.cipher = None
        self.keys = None


    def generate_keys(self):
        bin_key = '{:064b}'.format(int(self.__key, 16))    # 原始密钥二进制字符串
        key = ''.join([bin_key[index - 1] for index in PC1])    #原始密钥变换后二进制字符串
        print('///'+key)
        c0 = key[0:28]  # 生成用密钥种子1
        d0 = key[28:]   # 生成用密钥种子2
        c = [cycle_Lshift(c0, LShift[0])]
        d = [cycle_Lshift(d0, LShift[0])] 
        self.keys = []   # 实际使用密钥列表，每个元素为二进制整数
        for time in range(1, self.__rounds):
            c.append(cycle_Lshift(c[time - 1], LShift[time]))
            d.append(cycle_Lshift(d[time - 1], LShift[time]))
        self.keys = [int(''.join([(c[i] + d[i])[index - 1] for index in PC2]), 2) for i in range(self.__rounds)]

    def encrypt(self):
        keys = self.generate_keys()
        left = self.bin_message[0:32]
        right = self.bin_message[32:]
        for i in range(self.__rounds):
            left, right = right, '{:032b}'.format(int(left, 2) ^ f(right, self.keys[i]))
        self.cipher = left + right

    def get_l0(self):
        return self.bin_message[0:32]

    def get_r0(self):
        return self.bin_message[32:]

    def get_l3(self):
        return self.cipher[0:32]

    def get_r3(self):
        return self.cipher[32:]

    def get_el3(self):
        e = ''.join([self.get_l3()[index - 1] for index in E])
        # print([e[i:i + 6] for i in range(0, 48, 6)])
        return [int(e[i:i + 6], 2) for i in range(0, 48, 6)]

    def get_rounds(self):
        return self.__rounds

class Couple_Pair(object):
    def __init__(self, mcp1, mcp2):
        self.mcp1 = mcp1
        self.mcp2 = mcp2
        mcp1.encrypt()
        mcp2.encrypt()
        print('{:016x}'.format(int(mcp1.cipher, 2)))
        print('{:016x}'.format(int(mcp2.cipher, 2)))
        self.input_xor = [mcp1.get_el3()[i] ^ mcp2.get_el3()[i] for i in range(8)]
        # print(self.input_xor)
        self.r3_xor = int(mcp1.get_r3(), 2) ^ int(mcp2.get_r3(), 2)
        self.l0_xor = int(mcp1.get_l0(), 2) ^ int(mcp2.get_l0(), 2)
        output_xor_temp = ''.join(['{:032b}'.format(self.r3_xor ^ self.l0_xor)[index - 1] for index in P_1])
        self.output_xor = [int(output_xor_temp[i:i + 4], 2) for i in range(0, 32, 4)]
        # print(self.output_xor)
        self.inout_list = []
        self.test = []
        # print("=" * 20)

    def generate_inout_list(self):
        for i in range(8):
            self.inout_list.append({})
            # key: input_xor, value: (key: output_xor, value: set())
            for input_xor in range(64):
                self.inout_list[i][input_xor] = {}
                for input_b in range(64):
                    output_xor = int(s_box(input_b, i), 2) ^ int(s_box(input_b ^ input_xor, i), 2)
                    if not self.inout_list[i][input_xor].get(output_xor):
                        self.inout_list[i][input_xor][output_xor] = set()
                    self.inout_list[i][input_xor][output_xor].add(input_b)

    def generate_test(self):
        for i in range(8):
            try:
                self.test.append(set())
                for k in self.inout_list[i][self.input_xor[i]][self.output_xor[i]]:
                    self.test[i].add(k ^ self.mcp1.get_el3()[i])
                if i == 3:
                    print(self.input_xor[i])
                    print(self.output_xor[i])
                    print(self.mcp2.cipher)
                    print(self.mcp1.get_l3())
                    print(self.mcp2.get_l3())
            except Exception:
                print(i)
                print(self.input_xor[i])
                print(self.output_xor[i])
                print(self.mcp1.get_el3()[i])
                print(self.mcp2.get_el3()[i])
                sys.exit()


    def get_test(self):
        return self.test


class Attack(object):
    def __init__(self, couple1, couple2, couple3):
        self.couple1 = couple1
        self.couple2 = couple2
        self.couple3 = couple3
        self.keys = []
        self.final_key = None
    
    def attack(self):
        # print("//1")
        self.couple1.generate_inout_list()
        self.couple1.generate_test()
        # print("//2")
        self.couple2.generate_inout_list()
        self.couple2.generate_test()
        # print("//3")
        self.couple3.generate_inout_list()
        self.couple3.generate_test()
        for i in range(8):
            self.keys.append(set())
            self.keys[i] = set.intersection(
                self.couple1.get_test()[i], self.couple2.get_test()[i], self.couple3.get_test()[i])
        self.enum_final_key()
    
    def enum_final_key(self):
        bin_key48 = ''.join('{:06b}'.format(list(self.keys[i])[0]) for i in range(8))
        PC2_rev = [100] * 56
        for i in range(len(PC2)):
            PC2_rev[PC2[i] - 1] = bin_key48[i]
        # print(PC2_rev)
        omit_index = []
        for i in range(len(PC2_rev)):
            if PC2_rev[i] == 100:
                omit_index.append(i)
        # print(omit_index)
        for insert in range(1<<8):
            insert_list = '{:08b}'.format(insert)
            for i in range(len(omit_index)):
                PC2_rev[omit_index[i]] = insert_list[i]
            # 逆PC2_rev到初始56bit
            key_temp = ''.join(PC2_rev)
            key_generate_list = [int(bin_key48, 2)]
            shift_time = 0
            for t in range(2, 0, -1):
                key_temp = cycle_Rshift(key_temp[0:28], LShift[t]) + cycle_Rshift(key_temp[28:], LShift[t])
                key_generate_list.insert(0, int(''.join([key_temp[index - 1] for index in PC2]), 2))
            key_temp = cycle_Rshift(key_temp[0:28], LShift[0]) + cycle_Rshift(key_temp[28:], LShift[0])
            message = '{:064b}'.format(int(self.couple1.mcp1.message, 16))
            left = message[0:32]
            right = message[32:]
            for i in range(3):
                left, right = right, '{:032b}'.format(int(left, 2) ^ f(right, key_generate_list[i]))
            if left + right == self.couple1.mcp1.cipher:
                self.final_key = key_temp

    def get_final_key(self):
        return self.final_key

if __name__ == '__main__':
    '''
    message_11 = "1049f89a13579ace"
    message_12 = "bacbeeba13579ace"
    message_21 = "90184950eca97531"
    message_22 = "bacbeebaeca97531"
    message_31 = "0948173411514611"
    message_32 = "bacbeeba11514611"
    '''
    src = open("differential.txt", "r")
    src_list = src.readlines()
    (message_11, cipher_11, message_12, cipher_12, message_21, cipher_21, message_22, cipher_22, 
        message_31, cipher_31, message_32, cipher_32) = [s[:-1] for s in src_list]
    couple1 = Couple_Pair(Message_Cipher_Pair(message_11), Message_Cipher_Pair(message_12))
    couple2 = Couple_Pair(Message_Cipher_Pair(message_21), Message_Cipher_Pair(message_22))
    couple3 = Couple_Pair(Message_Cipher_Pair(message_31), Message_Cipher_Pair(message_32))
    crack = Attack(couple1, couple2, couple3)
    crack.attack()
    cracked_key = crack.get_final_key()
    print(cracked_key)
                