IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_1 = [4, 1, 3, 5, 7, 2, 8, 6]
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
E = [4, 1, 2, 3, 2, 3, 4, 1]
P4 = [2, 4, 3, 1]
S1 = [1, 0, 3, 2, 3, 2, 1, 0, 0, 2, 1, 3, 3, 1, 0, 2]
S2 = [0, 1, 2, 3, 2, 0, 1, 3, 3, 2, 1, 0, 2, 1, 0, 3]
SBOX = [S1, S2]
# S-DES加密部分
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

# S_DES明密文对类，包含加密和取值方法
class S_DES_Pair(object):
    def __init__(self, message):
        self.src_key = None
        self.src_message = message
        self.cipher = None
        self.keys = None

    def generate_keys(self):
        self.keys = None
        bin_key = '{:010b}'.format(self.src_key)    # 原始密钥二进制字符串
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

# S_DES中间相遇攻击类，包含明密文对和攻击方法
class S_DES_MITM(object):
    def __init__(self, pair1, pair2, pair3):
        self.pair_src = pair1
        self.pair_test1 = pair2
        self.pair_test2 = pair3
        self.input_dict = {}
        self.final_key = []
        self.encrypt_atk = None
        self.decrypt_atk = None

    def attack(self):
        self.encrypt_atk = S_DES_Pair(self.pair_src[0])
        self.decrypt_atk = S_DES_Pair(self.pair_src[1])
        # 打加密表
        for test_key1 in range(1<<10):
            self.encrypt_atk.set_key(test_key1)
            self.encrypt_atk.generate_keys()
            self.encrypt_atk.encrypt()
            #self.input_dict[test_key1] = self.encrypt_atk.get_cipher()
            if self.input_dict.get(self.encrypt_atk.get_cipher(), None) == None:
                self.input_dict[self.encrypt_atk.get_cipher()] = [test_key1]
            else:
                self.input_dict[self.encrypt_atk.get_cipher()].append(test_key1)
        # 开始测试相遇
        for test_key2 in range(1<<10):
            self.decrypt_atk.set_key(test_key2)
            self.decrypt_atk.generate_keys()
            self.decrypt_atk.keys = self.decrypt_atk.keys[::-1]
            self.decrypt_atk.encrypt()
            # 相遇后用其他的明密文对进行验证
            if self.decrypt_atk.get_cipher() in self.input_dict.keys():
                #maybe_key1 = list(self.input_dict.keys())[list(self.input_dict.values()).index(self.decrypt_atk.get_cipher())]
                maybe_key1 = self.input_dict[self.decrypt_atk.get_cipher()]
                maybe_key2 = test_key2
                for k1 in maybe_key1:
                    if self.check(k1, maybe_key2):
                        self.final_key.append((k1, maybe_key2))
    # 验证方法
    def check(self, key1, key2):
        check11 = S_DES_Pair(self.pair_test1[0])
        check11.set_key(key1)
        check11.generate_keys()
        check11.encrypt()
        check12 = S_DES_Pair(check11.get_cipher())
        check12.set_key(key2)
        check12.generate_keys()
        check12.encrypt()
        if check12.get_cipher() != self.pair_test1[1]:
            return False
        check21 = S_DES_Pair(self.pair_test2[0])
        check21.set_key(key1)
        check21.generate_keys()
        check21.encrypt()
        check22 = S_DES_Pair(check21.get_cipher())
        check22.set_key(key2)
        check22.generate_keys()
        check22.encrypt()
        if check22.get_cipher() != self.pair_test2[1]:
            return False
        return True


if __name__ == '__main__':
    src = open("MITM.txt", "r")
    src_list = src.readlines()
    (message_1, cipher_1, message_2, cipher_2, 
        message_3, cipher_3) = [s[:-1] for s in src_list]
    attack = S_DES_MITM((message_1, cipher_1), (message_2, cipher_2), (message_3, cipher_3))
    attack.attack()
    print("The probable key pairs(in decimal):")
    for k_pair in attack.final_key:
        print(k_pair)
    

        