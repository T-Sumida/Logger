# -*- coding:utf-8 -*-
import tkinter as tk
from tkinter import filedialog as tkFileDialog
import tkinter.scrolledtext
from tkinter import Toplevel
import os,sys
import datetime

CONFIGFILE_NAME = "config.txt"
LOGDIR_NAME = "/Log"

class FileManager:
    """ ファイル関連を管理するクラス """
    
    def __init__(self):
        self.rootDirPath=''
        self.initProcess()
        

    def initProcess(self):
        self.checkExistFile(CONFIGFILE_NAME)

        with open(CONFIGFILE_NAME) as f:
            self.rootDirPath = f.read()

        if self.rootDirPath == "":
            self.selectRootDir()
            with open(CONFIGFILE_NAME,'w') as f:
                f.write(self.rootDirPath)

        if os.path.isdir(self.rootDirPath + LOGDIR_NAME) == False:
            print(self.rootDirPath+LOGDIR_NAME)
            os.mkdir(self.rootDirPath+LOGDIR_NAME)


    def writeLog(self,contents):
        now = datetime.datetime.now()
        dirname = self.rootDirPath + LOGDIR_NAME + '/{0:%Y}'.format(now)
        filename = dirname + '/{0:%m%d}.txt'.format(now)
        if os.path.isdir(dirname) == False:
            os.mkdir(dirname)
        self.checkExistFile(filename)
        with open(filename,'a') as f:
                f.write('\n-------- {0:%H:%M:%S}--------\n'.format(now))
                f.write(contents)

    def checkExistFile(self,filepath):
        if os.path.isfile(filepath) == False:
            with open(filepath,'w') as f:
                f.write("")

    def selectRootDir(self):
        root = tkinter.Tk()
        root.withdraw()

        # Make it almost invisible - no decorations, 0 size, top left corner.
        root.overrideredirect(True)
        root.geometry('0x0+0+0')

        # Show window again and lift it to top so it can get focus,
        # otherwise dialogs will end up behind the terminal.
        root.deiconify()
        root.lift()
        root.focus_force()

        self.rootDirPath = tkFileDialog.askdirectory(parent=root) # Or some other dialog

        # Get rid of the top-level instance once to make it actually invisible.
        root.destroy()


class Logger(tkinter.Frame):
    """ Logger本体クラス"""

    def __init__(self,master=None):
        tkinter.Frame.__init__(self,master)
        self.font = 'メイリオ'
        self.master.title("Logger")
        self.config(width=20,height=20)

        self.fileMgr = FileManager()

        self.createTextField()
        self.createMenu()
        self.master.configure(menu=self.menu)

        self.master.bind("<Control-Key-s>",self.save)

        self.pack()



    def createTextField(self):
        self.txt = tkinter.scrolledtext.ScrolledText(self.master,width=30, height=10, font=(self.font, '15'))
        self.txt.pack(fill=tkinter.BOTH, expand=1)

    def createMenu(self):
        self.menu = tkinter.Menu(self.master)
        me = tkinter.Menu(self.master)
        me.add_command(label='new')
        self.menu.add_cascade(menu=me,label='file')

    def save(self,event):
        self.fileMgr.writeLog(self.txt.get('1.0', tk.END))
        self.txt.delete('1.0',tk.END)

    def load(self,event):
        print('r')

    def changeRootDir(self,event):
        print('c')
        


if __name__=="__main__":
    root = tkinter.Tk()
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    m = Logger()
    m.mainloop()