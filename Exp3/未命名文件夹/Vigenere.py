# Vigenere Cipher
def mod26(letter):
    return ord(letter.upper()) - ord('A')

def VigenereCipher(message, key):
    cipher = []
    lenK = len(key)
    for i in range(len(message)):
        temp = mod26(message[i]) + mod26(key[i % lenK])
        cipher.append(chr(temp % 26 + ord('A')))
    return ''.join(cipher)

def VigenereDecrypt(cipher, key):
    message = []
    lenK = len(key)
    for i in range(len(cipher)):
        temp = mod26(cipher[i]) - mod26(key[i % lenK])
        message.append(chr(temp % 26 + ord('A')))
    return ''.join(message)

def main():
    print("Input message:")
    message = input()
    while True:                                     
        print("Input key:")
        key = input()
        if len(key) <= len(message):
            break
        else:
            print("Key too long!")
    print("Encrypt finished. The cipher is:")
    cipher = VigenereCipher(message, key)
    print(cipher)
    print()
    print("=" * 20)
    print()
    while True:
        print("Input the key to decrypt:")
        keyd = input()
        if keyd.upper() == key.upper():
            print(VigenereDecrypt(cipher, key))
            break
        else:
            print("Seem to be the wrong key.")
    

if __name__ == '__main__':
    main()
    
