import tkinter as tk
from tkinter import *
from tkinter import filedialog
from RSA import *
from RSAKey import *
from time import time

class App(object):
    def __init__(self, root):
        self.root = root
        self.fileName = None
        self.root.geometry("600x200")
        self.frame = Frame(self.root)
        self.buttonEncrypt = Button(self.frame, text="加密", command = self.encrypt)
        self.buttonDecrypt = Button(self.frame, text="解密", command = self.decrypt)
        self.buttonBrowse = Button(self.frame, text="浏览", command = self.openFile)
        self.buttonGenerate = Button(self.frame, text="生成密钥", command = self.generate)
        self.labelAddr = Label(self.frame, text="文件地址：")
        self.textAddr = Entry(self.frame, width=40)
        self.frame.grid(column=0, row=1)
        self.labelAddr.grid(column=0, row=1)
        self.textAddr.grid(column=1, row=1)
        self.buttonBrowse.grid(column=2, row=1)
        self.buttonEncrypt.grid(column=2, row=2)
        self.buttonDecrypt.grid(column=3, row=2)
        self.buttonGenerate.grid(column=1, row=2)
    
    def generate(self):
        key = RSAKey()
        key.generateKey()

    def encrypt(self):
        start = time()
        encrypt = RSA(self.fileName)
        encrypt.setMsg()
        encrypt.encrypt()
        encrypt.outputCipher()
        end = time()
        print(end-start)

    def decrypt(self):
        start = time()
        decrypt = RSA(self.fileName)
        decrypt.setCip()
        decrypt.decrypt()
        decrypt.outputPlain()
        end = time()
        print(end-start)

    def openFile(self):
        self.fileName = tk.filedialog.askopenfilename(title="打开文件", 
            filetypes=[('Encrypted Files', '*.*Encrypted'), ('All Files', '*')])
        self.textAddr.delete(0, END)
        self.textAddr.insert(0, self.fileName)

root = Tk()
root.title("RSA")
app = App(root)
#btn1 = tk.Button(root, text='打开S2文件',font =("宋体",20,'bold'),width=13,height=8, command=openfiles2)
#btn1.pack(side="left")
root.mainloop()