import sys, getopt

# for encrypting
IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
IP_1 = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]
E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
P = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]
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
LShift = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
global rounds

def cycle_Lshift(string, n):
    return string[n:] + string[0:n]

# src_key: 十六进制比特串
def generate_key(src_key):
    global rounds
    bin_key = '{:064b}'.format(int(src_key, 16))    # 原始密钥二进制字符串
    key = ''.join([bin_key[index - 1] for index in PC1])    #原始密钥变换后二进制字符串
    c0 = key[0:28]  # 生成用密钥种子1
    d0 = key[28:]   # 生成用密钥种子2
    c = [cycle_Lshift(c0, LShift[0])]
    d = [cycle_Lshift(d0, LShift[0])] 
    keys = []   # 实际使用密钥列表，每个元素为二进制整数
    for time in range(1, rounds):
        c.append(cycle_Lshift(c[time - 1], LShift[time]))
        d.append(cycle_Lshift(d[time - 1], LShift[time]))
    keys = [int(''.join([(c[i] + d[i])[index - 1] for index in PC2]), 2) for i in range(rounds)]
    return keys

# right: 32bit, key: 48bit
def f(right, key):
    after_e = int(''.join([right[index - 1] for index in E]), 2)
    src_b = '{:048b}'.format(after_e ^ key)
    b = [src_b[i:i + 6] for i in range(0, 48, 6)]
    after_s = ''.join(['{:04b}'.format(SBOX[i][16 * int(b[i][0] + b[i][-1], 2) + int(b[i][1:-1], 2)]) 
        for i in range(8)])
    result = int(''.join([after_s[index - 1] for index in P]), 2)
    #result = int(''.join(after_s), 2)
    return result

# message: 十六进制比特串, keys: rounds个48bit密钥
def encrypt(src_message, keys):
    global rounds
    # keys = generate_key(src_key)
    bin_message = '{:064b}'.format(int(src_message, 16)) # 明文二进制字符串
    message = ''.join([bin_message[index - 1] for index in IP])
    left = message[0:32]
    right = message[32:]
    for i in range(rounds):
        left, right = right, '{:032b}'.format(int(left, 2) ^ f(right, keys[i]))
    final = right + left
    cipher = int(''.join([final[index - 1] for index in IP_1]), 2)
    return '{:016x}'.format(cipher)

def useage():
    print("Useage: %s [-m|--message] message [-c|--cipher] cipher [-k|--key] key [-r|--rounds] rounds(default 16)")
    sys.exit()
 
if __name__ == '__main__':
    global rounds
    rounds = 16
    try:
        have_message = False
        have_key = False
        have_cipher = False
        opts, args = getopt.getopt(sys.argv[1:], "hm:c:k:r:", ["help", "message=", "cipher=", "key=", "rounds="])
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                useage()
            elif opt in ("-m", "--message"):
                message = arg
                have_message = True
            elif opt in ("-c", "--cipher"):
                cipher = arg
                have_cipher = True
            elif opt in ("-k", "--key"):
                key = arg
                have_key = True
            elif opt in ("-r", "--rounds"):
                rounds = int(arg)
            else:
                print("Unknown argument.")
                useage()
        if (not have_key or not (have_cipher or have_message)):
            print("More arguments are required.")
            useage()
        if (have_message):
            print("DES ENCRYPTOR")
            print("=" * 20)
            print("Your message is: " + message)
            print("Your key is: " + key)
            cipher_generated = encrypt(message, generate_key(key))
            print("Encrypt finished. Your cipher is: " + cipher_generated)
            print("")
        if (have_cipher):
            print("DES_DECRYPTOR")
            print("=" * 20)
            print("Your cipher is: " + cipher)
            print("Your key is: " + key)
            message_generated = encrypt(cipher, generate_key(key)[::-1])
            print("Decrypt finished. Your message is: " + message_generated)
            print("")
        print("Task completed.")

    except Exception:
        print("Argument error.")
        useage()
