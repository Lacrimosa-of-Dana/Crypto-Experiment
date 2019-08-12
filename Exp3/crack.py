from random import *
dic_high = {'e': 0.12702, 't': 0.09056}
dic_medium = {'a': 0.08167, 'o': 0.07507, 'i': 0.06966, 'n': 0.06749, }
dic_low = {'s': 0.06327, 'h': 0.06094,
       'r': 0.05987, 'd': 0.04253, 'l': 0.04025, 'c': 0.02782,
       'u': 0.02758, 'm': 0.02406, 'w': 0.02360, 'f': 0.02228,
       'g': 0.02015, 'y': 0.01974, 'p': 0.01929, 'b': 0.01492,
       'v': 0.00978, 'k': 0.00772, 'j': 0.00153, 'x': 0.00150,
       'q': 0.00095, 'z': 0.00074}
order = [[0, 1, 2, 3], [0, 1, 3, 2], [0, 2, 1, 3], [0, 2, 3, 1], [0, 3, 1, 2],
         [0, 3, 2, 1], [1, 0, 2, 3], [1, 0, 3, 2], [1, 2, 0, 3], [1, 2, 3, 0],
         [1, 3, 0, 2], [1, 3, 2, 0], [2, 0, 1, 3], [2, 0, 3, 1], [2, 1, 0, 3],
         [2, 1, 3, 0], [2, 3, 0, 1], [2, 3, 1, 0], [3, 0, 1, 2], [3, 0, 2, 1],
         [3, 1, 0, 2], [3, 1, 2, 0], [3, 2, 0, 1], [3, 2, 1, 0]]
def no_sig(src):
    c = ''
    for s in src:
        s = s.lower()
        if s >= 'a' and s <= 'z':
            c += s
    return c

def generate(message):
    message = no_sig(message)
    keye = {}
    src = list(range(26))
    for i in range(26):
        m = randint(0, len(src) - 1)
        keye[chr(ord('a') + i)] = chr(src[m] + ord('a'))
        src.pop(m)
    cipher = ''
    for s in message:
        cipher += keye[s]
    return keye, cipher




def statistics(cipher):
    rst = {}
    for c in cipher:
        if rst.get(c, 0) == 0:
            rst[c] = 1
        else:
            rst[c] += 1
    for k in rst.keys():
        rst[k] /= len(cipher)
    statis = list(zip(rst.keys(), rst.values()))
    statis = sorted(statis, key = lambda x: x[1], reverse = True)
    return statis

def crack(cipher):
    probab = statistics(cipher)
    
    for i in range(2):
        keyd = {}
        keyd[probab[i][0]] = list(dic_high.keys())[0]
        keyd[probab[not i][0]] = list(dic_high.keys())[1]
        for j in range(len(order)):
            for k in range(4):
                keyd[probab[k + 2][0]] = list(dic_medium.keys())[order[j][k]]

            for r in range(6, len(probab)):
                keyd[probab[r][0]] = list(dic_low.keys())[r - 6]
            for c in cipher:
                print(keyd[c], end='')
            print('')
def main():
    message = input()
    key, cipher = generate(message)
    print(key)
    print(cipher)
    crack(cipher)

if __name__ == '__main__':
    main()
