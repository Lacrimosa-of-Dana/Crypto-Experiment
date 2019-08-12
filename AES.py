from util import *
from copy import deepcopy
class Word(object):
    def __init__(self, intList):
        self.word = intList

    def g(self, round):
        tempWord = Word(self.word)
        tempWord.word = self.word[1:] + [self.word[0]]
        tempWord.word = [S_BOX[integer//16][integer%16] for integer in tempWord.word]
        tempWord.word[0] ^= RC[round]
        return tempWord
        
    def getWord(self):
        return self.word

    def wordXor(self, w):
        return Word([self.word[i] ^ w.getWord()[i] for i in range(4)])


class Key(object):
    def __init__(self, key_32):
        self.key = key_32
        seperate = [key_32[i:i+2] for i in range(0, 32, 2)]
        self.wordList = [Word([int(sp, 16) for sp in seperate[i:i+4]]) for i in range(0, 16, 4)]
        self.wordList += [0] * 40
    
    def generateKey(self):
        for flag in range(4, 44):
            if flag % 4 == 0:
                self.wordList[flag] = self.wordList[flag-4].wordXor(self.wordList[flag-1].g(flag//4 - 1))
            else:
                self.wordList[flag] = self.wordList[flag-4].wordXor(self.wordList[flag-1])

    def getRoundKey(self, round):
        temp = [deepcopy(word.getWord()) for word in self.wordList[round*4:round*4+4]]
        for i in range(4):
            for j in range(i, 4):
                temp[i][j], temp[j][i] = temp[j][i], temp[i][j]
        return temp

class State(object):
    # plain_32: 32位十六进制字符串，共128bits
    # 构造state矩阵，每个元素为整数
    def __init__(self):
        self.plain = None
        self.matrix = [[0] * 4 for i in range(4)]

    def set(self, plain_32):
        self.plain = plain_32
        seperate = [plain_32[i:i+2] for i in range(0, 32, 2)]
        flag = 0
        #self.matrix = [[0] * 4 for i in range(4)]
        for j in range(4):
            for i in range(4):
                self.matrix[i][j] = int(seperate[flag], 16)
                flag += 1
                
    # 字节代替
    def substitute(self):
        for i in range(4):
            for j in range(4):
                temp = self.matrix[i][j]
                self.matrix[i][j] = S_BOX[temp//16][temp%16]
                #print(self.matrix)

    def revSubstitute(self):
        for i in range(4):
            for j in range(4):
                temp = self.matrix[i][j]
                self.matrix[i][j] = REV_S_BOX[temp//16][temp%16]

    # 行变换
    def shiftRows(self):
        self.matrix[1] = self.matrix[1][1:] + [self.matrix[1][0]]
        self.matrix[2] = self.matrix[2][2:] + self.matrix[2][:2]
        self.matrix[3] = [self.matrix[3][3]] + self.matrix[3][:3]

    def revShiftRows(self):
        self.matrix[1] = [self.matrix[1][-1]] + self.matrix[1][:-1]
        self.matrix[2] = self.matrix[2][2:] + self.matrix[2][:2]
        self.matrix[3] = self.matrix[3][1:] + [self.matrix[3][0]]

    # 列混淆
    def mixColumn(self):
        temp = [["0"] * 4 for i in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    temp[i][j] = add(temp[i][j], 
                        multiply(int_to_bin(mixColumnTable[i][k]), int_to_bin(self.matrix[k][j])))
        for i in range(4):
            for j in range(4):
                self.matrix[i][j] = int(temp[i][j], 2)

    def revMixColumn(self):
        temp = [["0"] * 4 for i in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    temp[i][j] = add(temp[i][j], 
                        multiply(int_to_bin(revMixColumnTable[i][k]), int_to_bin(self.matrix[k][j])))
        for i in range(4):
            for j in range(4):
                self.matrix[i][j] = int(temp[i][j], 2)

    # 轮密钥加
    def addRoundKey(self, key):
        for i in range(4):
            for j in range(4):
                self.matrix[i][j] ^= key[i][j]

    def revAddRoundKey(self, key):
        temp = [["0"] * 4 for i in range(4)]
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    temp[i][j] = add(temp[i][j], 
                        multiply(int_to_bin(revMixColumnTable[i][k]), int_to_bin(key[k][j])))
        for i in range(4):
            for j in range(4):
                key[i][j] = int(temp[i][j], 2)
                self.matrix[i][j] ^= key[i][j]

    def outputCipher(self):
        temp = [[self.matrix[i][j] for j in range(4)] for i in range(4)]
        for i in range(4):
            for j in range(i, 4):
                temp[i][j], temp[j][i] = temp[j][i], temp[i][j]
        return ''.join([''.join([int_to_hex(elm, 2) for elm in row]) for row in temp])

class AES(object):
    #def __init__(self, plain_32, key_32):
    #    self.state = State(plain_32)
    #    self.key = Key(key_32)
    #    self.key.generateKey()

    def __init__(self):
        self.state = State()
        self.key = None

    def set(self, plain_32, key):
        self.state.set(plain_32)
        self.key = key

    def encrypt(self):
        for round in range(11):
            #print([[int_to_hex(j, 2) for j in k]for k in self.key.getRoundKey(round)])
            if round == 0:
                self.state.addRoundKey(self.key.getRoundKey(round))
                #print(self.state.matrix)
            else:
                self.state.substitute()
                #print(self.state.matrix)
                self.state.shiftRows()
                #print(self.state.matrix)
                if round != 10:
                    self.state.mixColumn()
                    #print(self.state.matrix)
                self.state.addRoundKey(self.key.getRoundKey(round))
                #print(self.state.matrix)
            #print(self.state.outputCipher())

    def decrypt(self):
        for round in range(10, -1, -1):
            if round == 10:
                self.state.addRoundKey(self.key.getRoundKey(round))
                #print(self.state.matrix)
            else:
                self.state.revSubstitute()
                #print(self.state.matrix)
                self.state.revShiftRows()
                #print(self.state.matrix)
                if round != 0:
                    self.state.revMixColumn()
                    #print(self.state.matrix)
                    self.state.revAddRoundKey(self.key.getRoundKey(round))
                    
                    #print(self.state.matrix)
                else:
                    self.state.addRoundKey(self.key.getRoundKey(round))
                    #print(self.state.matrix)

    def getCipher(self):
        #print("//")
        return self.state.outputCipher()

if __name__ == '__main__':
    key = Key("0f1571c947d9e8590cb7add6af7f6798")
    key.generateKey()
    a = AES()
    a.set("0123456789abcdeffedcba9876543210", key)
    a.encrypt()
    #b.decrypt()
    print("Plain:", end='')
    print(a.state.plain)
    print("Key:", end='')
    print(key.key)
    print("Cipher:", end='')
    print(a.getCipher())
    #print(b.getCipher())

        