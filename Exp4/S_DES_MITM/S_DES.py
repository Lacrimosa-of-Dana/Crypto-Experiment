IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_1 = [4, 1, 3, 5, 7, 2, 8, 6]
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
E = [4, 1, 2, 3, 2, 3, 4, 1]
P4 = [2, 4, 3, 1]
S1 = [1, 0, 3, 2, 3, 2, 1, 0, 0, 2, 1, 3, 3, 1, 0, 2]
S2 = [0, 1, 2, 3, 2, 0, 1, 3, 3, 2, 1, 0, 2, 1, 0, 3]
SBOX = [S1, S2]

def cycle_Lshift(string, n):
    return string[n:] + string[0:n]

def f(right, key):
    after_e = int(''.join([right[index - 1] for index in E]), 2)
    src_b = '{:08b}'.format(after_e ^ key)
    b = [src_b[0:4], src_b[4:]]
    after_s = ''.join(['{:02b}'.format(SBOX[i][4 * int(b[i][0] + b[i][-1], 2) + int(b[i][1:-1], 2)]) 
        for i in range(2)])
    result = int(''.join([after_s[index - 1] for index in P4]), 2)
    return result

class S_DES_Pair(object):
    def __init__(self, message):
        self.src_key = None
        self.src_message = message
        self.cipher = None
        self.keys = None

    def generate_keys(self):
        self.keys = None
        bin_key = '{:010b}'.format(int(self.src_key, 16))    # 原始密钥二进制字符串
        key = ''.join([bin_key[index - 1] for index in P10])    #原始密钥变换后二进制字符串
        c0 = key[0:5]  # 生成用密钥种子1
        d0 = key[5:]   # 生成用密钥种子2
        c = [cycle_Lshift(c0, 1), cycle_Lshift(c0, 3)]
        d = [cycle_Lshift(d0, 1), cycle_Lshift(d0, 3)] 
        self.keys = []   # 实际使用密钥列表，每个元素为二进制整数
        self.keys = [int(''.join([(c[i] + d[i])[index - 1] for index in P8]), 2) for i in range(2)]

    def encrypt(self):
        bin_message = '{:08b}'.format(int(self.src_message, 16)) # 明文二进制字符串
        message = ''.join([bin_message[index - 1] for index in IP])
        left = message[0:4]
        right = message[4:]
        for i in range(2):
            left, right = right, '{:04b}'.format(int(left, 2) ^ f(right, self.keys[i]))
        final = right + left
        self.cipher = '{:02x}'.format(int(''.join([final[index - 1] for index in IP_1]), 2))

    def set_key(self, key):
        self.src_key = key

    def get_cipher(self):
        return self.cipher

    def get_keys(self):
        return self.keys

class Double_S_DES(object):
    def __init__(self, pair, key1, key2):
        self.source = pair
        self.cipher1 = None
        self.cipher2 = None
        self.temp = None
        self.key1 = key1
        self.key2 = key2

    def encrypt(self):
        self.source.set_key(self.key1)
        self.source.generate_keys()
        self.source.encrypt()
        self.cipher1 = self.source.get_cipher()
        self.temp = S_DES_Pair(self.cipher1)
        self.temp.set_key(self.key2)
        self.temp.generate_keys()
        self.temp.encrypt()
        self.cipher2 = self.temp.get_cipher()

    def get_cipher(self):
        return self.cipher2

class S_DES_MITM(object):
    __key1 = "276"
    __key2 = "3b1"
    def __init__(self):
        self.encrypt_atk = None
        self.decrypt_atk = None
        self.atk_double = None
        #self.standard_double = Double_S_DES(S_DES_Pair("28"), self.__key1, self.__key2)
        #self.standard_double.encrypt()
        #self.test_double = S_DES_Pair("28")
        self.final_key1 = None
        self.final_key2 = None

    def attack(self):
        self.encrypt_atk = S_DES_Pair("41")
        self.atk_double = Double_S_DES(self.encrypt_atk, self.__key1, self.__key2)
        self.atk_double.encrypt()
        print(self.atk_double.get_cipher())
        self.decrypt_atk = S_DES_Pair(self.atk_double.get_cipher())
        for test_key1 in range(1<<10):
            for test_key2 in range(1<<10):
                key1 = hex(test_key1)[2:]
                key2 = hex(test_key2)[2:]
                self.encrypt_atk.set_key(key1)
                self.decrypt_atk.set_key(key2)
                self.encrypt_atk.generate_keys()
                self.decrypt_atk.generate_keys()
                self.decrypt_atk.keys = self.decrypt_atk.keys[::-1]
                self.encrypt_atk.encrypt()
                self.decrypt_atk.encrypt()
                if self.encrypt_atk.get_cipher() == self.decrypt_atk.get_cipher():
                    '''
                    for t in range(1<<8):
                        standard = Double_S_DES(S_DES_Pair(hex(t)[2:]), self.__key1, self.__key2)
                        perhaps = Double_S_DES(S_DES_Pair(hex(t)[2:]), key1, key2)
                        standard.encrypt()
                        perhaps.encrypt()
                        if standard.get_cipher() != perhaps.get_cipher():
                            break
                    else:
                        '''
                    print("0x" + key1 + ", 0x" + key2)

    def get_key(self): 
        return self.final_key1, self.final_key2

if __name__ == '__main__':
    #plain = Double_S_DES(S_DES_Pair("97"), "276", "3b1")
    #plain.encrypt()
    #print(plain.get_cipher())
    attack = S_DES_MITM()
    attack.attack()
    #print(attack.get_key())
