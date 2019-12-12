global format_num
def VernamCipher(message, key):
    global format_num
    cipher = []
    tempm = [('{:0' + str(format_num) + 'b}').format(ord(c)) for c in message]
    tempk = [('{:0' + str(format_num) + 'b}').format(ord(c)) for c in key]
    lenK = len(tempk)
    for i in range(len(tempm)):
        cipher.append(('{:0' + str(format_num) + 'b}').format(int(tempm[i], 2) ^ int(tempk[i % lenK], 2)))
    return ''.join(cipher)

def VernamDecrypt(cipher, key):
    global format_num
    message = []
    tempc = [cipher[i : i+ 16] for i in range(0, len(cipher), format_num)]
    tempk = [('{:0' + str(format_num) + 'b}').format(ord(c)) for c in key]
    lenK = len(tempk)
    for i in range(len(tempc)):
        message.append(chr(int(tempc[i], 2) ^ int(tempk[i % lenK], 2)))
    
    return ''.join(message)

def main():
    global format_num
    print("You are encrypting Chinese(input 1) or English(input 2) ?")
    language = int(input())
    if language == 1:
        format_num = 16
    else:
        format_num = 8
    message = input()
    key = input()
    cipher = VernamCipher(message, key)
    print(cipher)
    print("=" * 20)
    while True:
        keyd = input()
        print(VernamDecrypt(cipher, keyd))
        if keyd != key:
            print("Seem like the wrong key.")
        else:
            print("Successfully decrypted!")
            break

if __name__ == '__main__':
    main()
