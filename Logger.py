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
        """
        コンストラクタ処理
        """
        self.rootDirPath=''
        self.initProcess()
        

    def initProcess(self):
        """
        初期化処理
        コンフィグファイルから設定を読み込み、Logger/[年]/[月日].txtを作る
        """
        self.checkExistFile(CONFIGFILE_NAME) #コンフィグファイルの存在を確認

        with open(CONFIGFILE_NAME) as f:
            self.rootDirPath = f.read() # Logを保存するディレクトリパスを取得

        if self.rootDirPath == "": # ディレクトリパスが無かったら、新しく設定する
            self.selectRootDir()
            with open(CONFIGFILE_NAME,'w') as f:
                f.write(self.rootDirPath)

        if os.path.isdir(self.rootDirPath + LOGDIR_NAME) == False: # Logディレクトリが無かったら新しく作成する
            print(self.rootDirPath+LOGDIR_NAME)
            os.mkdir(self.rootDirPath+LOGDIR_NAME)


    def write(self,contents):
        """
        引数に与えられた内容を、保存時の[年]/[月日].txtに、時間と共に書き込む
        """
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
        """
        ファイルの存在をチェックする
        無かったら新しく作成する
        """
        if os.path.isfile(filepath) == False:
            with open(filepath,'w') as f:
                f.write("")

    def changeRootDirPath(self):
        """
        ログ保存ディレクトリを選択し直す
        """
        with open(CONFIGFILE_NAME,'w') as f:
                f.write("")
        self.initProcess()



    def selectRootDir(self):
        """
        ログを保存するディレクトリを選択するダイアログを出す
        """
        root = tkinter.Tk()
        root.withdraw()

        root.overrideredirect(True)
        root.geometry('0x0+0+0')

        root.deiconify()
        root.lift()
        root.focus_force()

        self.rootDirPath = tkFileDialog.askdirectory(parent=root)
        root.destroy()


class Logger(tkinter.Frame):
    """ Logger本体クラス"""

    def __init__(self,master=None):
        """
        コンストラクタ
        初期化処理を行う
        """
        tkinter.Frame.__init__(self,master)  # Logger本体のフレームを初期化
        self.font = 'メイリオ'                # フォント設定
        self.master.title("Logger")          # フレームタイトルの設定
        self.config(width=20,height=20)      # フレームサイズの設定

        self.fileMgr = FileManager()         # ファイル管理クラスインスタンスを作成

        # ログ書き込み部とメニュー部の初期化
        self.createTextField()
        self.createMenu()
        self.master.configure(menu=self.menu)

        # キーバインド設定
        self.master.bind("<Control-Key-s>",self.save)
        self.master.bind("<Control-Key-r>",self.changeRootDir)

        self.pack()

    def createTextField(self):
        """
        テキストフィールドを作成する
        """
        self.txt = tkinter.scrolledtext.ScrolledText(self.master,width=30, height=10, font=(self.font, '15'))
        self.txt.pack(fill=tkinter.BOTH, expand=1)

    def createMenu(self):
        """
        メニューを作成する
        """
        self.menu = tkinter.Menu(self.master)
        me = tkinter.Menu(self.master)
        me.add_command(label='new')
        self.menu.add_cascade(menu=me,label='file')

    def save(self,event):
        """
        コールバック関数
        テキストフィールドにある文字列を保存する
        """
        self.fileMgr.write(self.txt.get('1.0', tk.END))
        self.txt.delete('1.0',tk.END)

    def changeRootDir(self,event):
        self.fileMgr.changeRootDirPath()
        


if __name__=="__main__":
    root = tkinter.Tk()
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    m = Logger()
    m.mainloop()