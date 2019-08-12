import tkinter as tk
from tkinter import *
from tkinter import filedialog
from CFB import *
from CBC import *
from time import time

class App(object):
    def __init__(self, root):
        self.root = root
        self.fileName = None
        self.root.geometry("600x400")
        self.frame = Frame(self.root)
        self.frameModel = Frame(self.root)
        self.buttonEncrypt = Button(self.frameModel, text="加密", command = self.encrypt)
        self.buttonDecrypt = Button(self.frameModel, text="解密", command = self.decrypt)
        self.buttonBrowse = Button(self.frame, text="浏览", command = self.openFile)
        self.textKey = Entry(self.frame, width=40)
        self.textIV = Entry(self.frame, width=40)
        self.labelIV = Label(self.frame, text="初始向量：")
        self.labelKey = Label(self.frame, text="密钥：")
        self.labelAddr = Label(self.frame, text="文件地址：")
        self.textAddr = Entry(self.frame, width=40)
        #self.chooseMode1 = Radiobutton(self.frameModel, text="CBC", variable=self.mode, value='CBC', command=lambda:self.mode="CBC")
        #self.chooseMode2 = Radiobutton(self.frameModel, text="CFB", variable=self.mode, value='CFB', command=lambda:self.mode="CFB")
        self.labelMode = Label(self.frameModel, text="加密模式（CBC或CFB）：")
        self.textMode = Entry(self.frameModel, width=20)

        self.frame.grid(column=0, row=1)
        self.frameModel.grid(column=0, row=2)
        self.labelKey.grid(column=0, row=1)
        self.textKey.grid(column=1, row=1)
        self.labelIV.grid(column=0, row=2)
        self.textIV.grid(column=1, row=2)
        self.labelAddr.grid(column=0, row=3)
        self.textAddr.grid(column=1, row=3)
        self.buttonBrowse.grid(column=2, row=3)
        self.buttonEncrypt.grid(column=2, row=0)
        self.buttonDecrypt.grid(column=3, row=0)
        #self.chooseMode1.grid(column=0, row=0)
        #self.chooseMode2.grid(column=1, row=0)
        self.labelMode.grid(column=0, row=0)
        self.textMode.grid(column=1, row=0)
    '''
    def encrypt(self):
        encrypt = CFB(self.fileName, self.textKey.get(), self.textIV.get())
        encrypt.encrypt("ENCRYPT")
        encrypt.output("ENCRYPT")
    def decrypt(self):
        decrypt = CFB(self.fileName, self.textKey.get(), self.textIV.get())
        decrypt.encrypt("DECRYPT")
        decrypt.output("DECRYPT")
    '''
    def encrypt(self):
        if self.textMode.get() == 'CBC':
            start = time()
            encrypt = CBC(self.fileName, self.textKey.get(), self.textIV.get())
            encrypt.encrypt()
            encrypt.output("ENCRYPT")
            end = time()
            print(end-start)
        elif self.textMode.get() == 'CFB':
            start = time()
            encrypt = CFB(self.fileName, self.textKey.get(), self.textIV.get())
            encrypt.encrypt("ENCRYPT")
            encrypt.output("ENCRYPT")
            end = time()
            print(end-start)
    def decrypt(self):
        if self.textMode.get() == 'CBC':
            start = time()
            decrypt = CBC(self.fileName, self.textKey.get(), self.textIV.get())
            decrypt.decrypt()
            decrypt.output("DECRYPT")
            end = time()
            print(end-start)
        elif self.textMode.get() == 'CFB':
            start = time()
            decrypt = CFB(self.fileName, self.textKey.get(), self.textIV.get())
            decrypt.encrypt("DECRYPT")
            decrypt.output("DECRYPT")
            end = time()
            print(end-start)
    def openFile(self):
        self.fileName = tk.filedialog.askopenfilename(title="打开文件", 
            filetypes=[('Encrypted Files', '*.*Encrypted'), ('All Files', '*')])
        self.textAddr.delete(0, END)
        self.textAddr.insert(0, self.fileName)

root = Tk()
root.title("AES")
app = App(root)
#btn1 = tk.Button(root, text='打开S2文件',font =("宋体",20,'bold'),width=13,height=8, command=openfiles2)
#btn1.pack(side="left")
root.mainloop()