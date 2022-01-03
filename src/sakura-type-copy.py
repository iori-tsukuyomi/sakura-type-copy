# !/usr/bin/python
# -*- coding: utf-8 -*-
# ===== サクラエディタ・タイプ別設定一括コピープログラム
"""サクラエディタ・タイプ別設定一括コピープログラム

サクラエディタに定義されているすべての「タイプ別設定」を、
選択した「タイプ別設定」の値に変更するプログラムです。
"""

__author__ = 'Iori Tsukuyomi'
__credit__ = 'Copyright (C) 2022 Iori Tsukuyomi All Rights Reserved.'
__date__ = '2022/01/03'
__version__ = '0.1.0'

import codecs
import configparser
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox

# ----- 定数宣言
ENC = 'utf_8_sig'
TITLE = 'サクラエディタ・タイプ別設定一括コピー'
COPY_ITEMS = [
    'C[BRC]',
    'C[CAR]',
    'C[CBK]',
    'C[CMT]',
    'C[CTL]',
    'C[CVL]',
    'C[DFA]',
    'C[DFC]',
    'C[DFD]',
    'C[EBK]',
    'C[EOF]',
    'C[EOL]',
    'C[FN2]',
    'C[FN3]',
    'C[FN4]',
    'C[FN5]',
    'C[FND]',
    'C[HDC]',
    'C[IME]',
    'C[KW1]',
    'C[KW2]',
    'C[KW3]',
    'C[KW4]',
    'C[KW5]',
    'C[KW6]',
    'C[KW7]',
    'C[KW8]',
    'C[KW9]',
    'C[KWA]',
    'C[LNO]',
    'C[MOD]',
    'C[MRK]',
    'C[NOT]',
    'C[NUM]',
    'C[PGV]',
    'C[RAP]',
    'C[RK1]',
    'C[RK2]',
    'C[RK3]',
    'C[RK4]',
    'C[RK5]',
    'C[RK6]',
    'C[RK7]',
    'C[RK8]',
    'C[RK9]',
    'C[RKA]',
    'C[RUL]',
    'C[SEL]',
    'C[SPC]',
    'C[SQT]',
    'C[TAB]',
    'C[TXT]',
    'C[UND]',
    'C[URL]',
    'C[VER]',
    'C[WQT]',
    'C[ZEN]',
    'nVertLineIdx1',
]
ICON_DATA = '''
R0lGODlhIAAgAHcAACH5BAEAAAUALAAAAAAgACAAhwAAAAD///8A/4CAgMDAwP//
8P///wAAALGApLGAtAAAAAAAAAAAArXynLGApATyyLS2a70qaMG/qxIikLg5cLGA
pAAAAAAAAAAAAAAAAAAAAAAAAAAAASgd0AAAAATzCAAAAAAAF7GApAAAAATyaAAA
AAT1zLXqQHmle////gTy0AAAAAAAATotYCGFxxsiQAAAAFcIKgAAAAAAAQAAAAAW
BSUEEATzCByEowTzKAAAAQCwKTotYATziGMVLOJM6ggVvwAABAT2EAUVyAAAAOJM
92MVLOJM6ggVvwAABAT2MAUVtQAAAOJM9wAAAEB/LAAAAATzrCBXt1cIKgCwKSBX
+wCwKQBgEDfHvFcIKkB/LAAAAQAAAATzfB5uJgT0rCJTQJJ/7P///gTz2CIzm1cI
KgCwKQAAAAAAAFcIKrqrzUB/LACwKVcIKgT0vCGjOkB/LKLxhAT0vCGlfyGjfLFD
GEB/LDotYAUAAAAAD2MQvOLZNGMSPIdrPAEVv4UADwEVvwEVvwAAAKMVv////wAz
7AGjATIc/AT0ZKMVv////wAz7AGjAYUADwAAAKMVv////wAz7AGjAT8AAAAAAAAA
AWMaTOMIbAT0pAABAAT0mId3bwT0pElBTnRhWEL8iAT0pAADAAAAAP//AP8A/4CA
gMDAwP///wAAAAAAAKSAsbSAsQAAAAAAAAIAAJzytaSAscjyBGu2tGgqvau/wZAi
EnA5uKSAsQAAAAAAAAAAAAAAAAAAAAAAAAEAANAdKAAAAAjzBAAAABcAAKSAsQAA
AGjyBAAAAMz1BEDqtXulef7//9DyBAAAAAEAAGAtOseFIUAiGwAAACoIVwAAAAEA
AAAAAAUWABAEJQjzBKOEHCjzBAEAACmwAGAtOojzBIgiEsCSHNKSHBD0BCwfY66z
szw7AGMUfOMFewgVvwAAAAABAAT2GAAAAgAAAGMUfOMFewgVvwAAAAABAAT2OAAA
AgAAAAT2GId2mGMaTAT2JAT2JOM3+QT2IAAABAAAAAj/AAsILAAAAEGDBQ8qTMhw
oEOBAwwMiDhRIsWLFjMOMPgwIgADBj6GBCmyJEmQGzd2HMnSZMuTEgGodBgRpM2b
OHMaICCT48CaAoIG1UmU58yfBoQqJZrTqE+ISZUObbqTAAGQTldKnZqxaE+tW3dO
HKszK82oQgmMXTv2qk2zSNEKYKuW7U24UHG2vUv27dezVa1OvNq3rtudf+PaJNsX
ZUWsifM6rjgYpcXHeAvUFNy284C6mCNr1luT7cWaiI/mtcoadFvDbjOjvrkXa+PU
T0cHBs2ZbmzRsy9PXnsY98qqr10TCMCcOWTVum2TNtC8unHATG1Wb349bmurObc7
K5ed/ab4AN1Xfw8vPn308tStuw8OH2dmzd/z62cNgOfDgQUFKOCABAb4UEAAOw==
'''


# ----- バイト文字列のエンコーディング取得
def encoding_detector(data: bytes) -> str:
    encodings = [
        'utf_8_sig', 'utf_8', 'utf_32',
        'cp932', 'shift_jis', 'shift_jisx0213',
        'euc_jp',
        'iso2022_jp', 'iso2022_jp_2',
        'latin_1', 'ascii',
    ]
    ret_encoding = None
    if isinstance(data, bytes):
        for encoding in encodings:
            try:
                str(data, encoding=encoding, errors='strict')
                ret_encoding = encoding
                break
            except UnicodeDecodeError:
                continue
    return ret_encoding


# ----- オブジェクトを文字列に変換する
def to_unistr(data: object, encoding=None) -> str:
    try:
        if data is None:
            return ''
        elif str(type(data)).find('datetime') > -1:
            return data.strftime('%Y-%m-%d %H:%M:%S')
        elif str(type(data)).find('time') > -1:
            return data.Format('%Y-%m-%d %H:%M:%S')
        elif isinstance(data, bytes):
            if encoding is None:
                encoding = encoding_detector(data)
            if encoding:
                return data.decode(encoding)
            else:
                return ''
        else:
            return str(data)
    except BaseException:
        return ''


# ----- スクリプト実行フォルダの取得
def get_pwd() -> str:
    if getattr(sys, "frozen", False):
        return os.path.abspath(os.path.dirname(sys.executable))
    else:
        return os.path.dirname(os.path.abspath(__file__))


# ----- iniファイルの内容を辞書として取得
def load_inifile(filename: str, encoding=ENC) -> configparser:
    try:
        cp = configparser.ConfigParser(empty_lines_in_values=True)
        cp.BasicInterpolation = None
        cp.optionxform = str
        cp.read(filename, encoding)
        return cp
    except BaseException:
        return None


# ----- テキストファイルを読み込み、各行をリストとして取得
def load_textfile(filename, encoding=ENC):
    if os.path.isabs(filename) is False:
        filename = os.path.join(get_pwd(), filename)
    if os.path.exists(filename):
        try:
            with open(filename, 'rb') as f:
                encoding = encoding_detector(f.read())
                if encoding is None:
                    encoding = ENC
            with codecs.open(filename, 'r', encoding) as f:
                lines = f.read().replace('\r', '').split('\n')
                return lines
        except BaseException:
            return None
    return None


# ----- リストのアイテムを行としてテキストファイルに出力
def save_textfile(data_list, filename, encoding=ENC, newline='\r\n'):
    if os.path.isabs(filename) is False:
        filename = os.path.join(get_pwd(), filename)
    try:
        with codecs.open(filename, 'w', encoding=encoding) as f:
            data = newline.join(data_list)
            f.write(data)
            return True
    except BaseException:
        return False
    return False


def get_setting_list(cp: configparser) -> dict:
    sec_key = 'Types({0})'
    pos = 0
    setting_list = {}
    try:
        while cp.has_section(sec_key.format(str(pos))):
            setting_list[cp[sec_key.format(str(pos))]['szTypeName']] = pos
            pos = pos + 1
    except BaseException:
        return None
    return setting_list


def get_item_list(filename: str, pos: int) -> dict:
    sec_key = '[Types({0})]'.format(str(pos))
    item_list = {}
    flag = 0
    datas = load_textfile(filename)
    for i in range(len(datas)):
        if flag == 1:
            for item in COPY_ITEMS:
                if datas[i].find(item) == 0:
                    item_list[item] = datas[i]
            if datas[i].find('[') == 0:
                break
        if datas[i].find(sec_key) == 0:
            flag = 1
    return item_list


def set_items(filename: str, item_list: dict, encoding=ENC) -> bool:
    flag = 0
    datas = load_textfile(filename, encoding=encoding)
    for i in range(len(datas)):
        if flag == 1:
            for key in item_list:
                if datas[i].lstrip().find(key) == 0:
                    datas[i] = item_list[key]
                    break
            if datas[i].lstrip().find('[') == 0:
                flag = 0
        if datas[i].lstrip().find('[Types(') == 0:
            flag = 1
    return datas


def main():
    filename = 'C:/sakura/sakura.ini'
    source_name = '基本'
    encoding = ENC
    # Check file existed.
    if os.path.isabs(filename) is False:
        filename = os.path.join(get_pwd(), filename)
        if os.path.exists(filename) is False:
            return False
    # Set endoding.
    with open(filename, 'rb') as f:
        encoding = encoding_detector(f.read())
        if encoding is None:
            encoding = ENC
    # Set config paser.
    cp = load_inifile(filename, encoding=encoding)
    if cp is None:
        return False
    # Set tyep list.
    type_list = get_setting_list(cp)
    if type_list is None:
        return False
    # Set copy items.
    item_list = get_item_list(filename, type_list[source_name])
    # Set ini file.
    save_textfile(
        set_items(
            filename,
            item_list,
            encoding=encoding),
        'C:/sakura/sakura-mod.ini',
        encoding=encoding)
    return item_list


class Application():
    def __init__(self, top=None):
        self.style = ttk.Style()
        self.style.theme_use('winnative')
        # self.style.configure('.',font="TkDefaultFont")
        top.geometry('580x100+150+150')
        top.resizable(0, 0)
        top.title('サクラエディタ・タイプ別設定一括コピー')

        self.top = top
        self.combobox = tk.StringVar()

        self.filename = ''
        self.encoding = ENC
        self.cp = None
        self.type_list = None

        self.TLabel1 = ttk.Label(self.top)
        self.TLabel1.place(x=10, y=10, height=19, width=75)
        # self.TLabel1.configure(font="TkDefaultFont")
        self.TLabel1.configure(relief='flat')
        self.TLabel1.configure(anchor='w')
        self.TLabel1.configure(justify='left')
        self.TLabel1.configure(text='設定ファイル名')
        self.TLabel1.configure(compound='left')

        self.entry_file = ttk.Entry(self.top)
        self.entry_file.place(x=90, y=10, height=21, width=406)
        self.entry_file.configure(state='readonly')
        self.entry_file.configure(takefocus='')
        self.entry_file.configure(cursor='fleur')

        self.TLabel2 = ttk.Label(self.top)
        self.TLabel2.place(x=10, y=40, height=19, width=68)
        # self.TLabel2.configure(font="TkDefaultFont")
        self.TLabel2.configure(relief='flat')
        self.TLabel2.configure(anchor='w')
        self.TLabel2.configure(justify='left')
        self.TLabel2.configure(text='コピー元タイプ')
        self.TLabel2.configure(compound='left')

        self.button_select = ttk.Button(self.top)
        self.button_select.place(x=500, y=10, height=25, width=76)
        self.button_select.configure(takefocus='')
        self.button_select.configure(text='選択')
        self.button_select.configure(compound='left')
        self.button_select.configure(command=self.get_filename)

        self.combobox_type = ttk.Combobox(self.top)
        self.combobox_type.place(x=90, y=40, height=21, width=403)
        self.combobox_type.configure(textvariable=self.combobox)
        self.combobox_type.configure(takefocus='')

        self.button_exec = ttk.Button(self.top)
        self.button_exec.place(x=420, y=70, height=25, width=76)
        self.button_exec.configure(takefocus='')
        self.button_exec.configure(text='実行')
        self.button_exec.configure(compound='left')
        self.button_exec.configure(command=self.set_item)

        self.button_quit = ttk.Button(self.top)
        self.button_quit.place(x=500, y=70, height=25, width=76)
        self.button_quit.configure(takefocus='')
        self.button_quit.configure(text='終了')
        self.button_quit.configure(compound='left')
        self.button_quit.configure(command=self.quit)

    def get_filename(self):
        self.filename = filedialog.askopenfilename(
            filetypes=[('設定ファイル', '*.*')])
        # Set endoding.
        with open(self.filename, 'rb') as f:
            self.encoding = encoding_detector(f.read())
            if self.encoding is None:
                self.encoding = ENC
        # Set config paser.
        self.cp = load_inifile(self.filename, encoding=self.encoding)
        if self.cp is None:
            messagebox.showerror(TITLE, '設定ファイルが読み込めませんでした。')
            return False
        # Set tyep list.
        self.type_list = get_setting_list(self.cp)
        if self.type_list:
            self.combobox_type.configure(values=list(self.type_list.keys()))
        else:
            messagebox.showerror(TITLE, 'タイプ別一覧が取得できませんでした。正しいファイルを選択してください。')
            return False
        self.entry_file.configure(state='normal')
        self.entry_file.delete(0, 'end')
        self.entry_file.insert(0, self.filename)
        self.entry_file.configure(state='readonly')

    def set_item(self):
        if self.combobox.get() == '':
            messagebox.showwarning(TITLE, 'コピー元タイプを選択してください。')
            return False
        ret = messagebox.askokcancel(
            TITLE, 'タイプ「{0}」の色指定と縦線桁指定をすべてのタイプに適用します。よろしいですか?'.format(
                self.combobox.get()))
        if ret:
            # Set copy items.
            item_list = get_item_list(
                self.filename, self.type_list[self.combobox.get()])
            if item_list:
                save_textfile(
                    set_items(
                        self.filename,
                        item_list,
                        encoding=self.encoding),
                    'C:/sakura/sakura-mod.ini',
                    encoding=self.encoding)
                messagebox.showinfo(TITLE, '正常に適用されました。アプリケーションを終了してください。')
            else:
                messagebox.showerror(
                    TITLE, '設定項目が取得できませんでした。正しいファイルを選択してください。')

    def quit(self):
        self.top.destroy()


# ----- 単体実行時の処理
if __name__ == '__main__':
    # param = load_inifile(create_tmp_file('C:/sakura/sakura.ini'))
    # cp = load_inifile('C:/sakura/sakura.ini')
    # save_inifile('C:/sakura/sakura-mod.ini', cp)
    # print(get_setting_list(cp))
    # print(main())
    root = tk.Tk()
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(data=ICON_DATA))
    # root.iconbitmap(default='C:/git-repos/sakura-type-copy/src/sakura-type-copy.ico')
    # app = Application(master=root)
    app = Application(top=root)
    root.mainloop()


# class Application(tk.Frame):
#     def __init__(self, master=None):
#         super().__init__(master)
#         self.master = master
#         self.master.geometry("640x480")
#         self.pack()
#         self.create_widgets()

#     def create_widgets(self):
#         self.frame_file = tk.Frame(self.master, padx=8, pady=8)
#         self.frame_select = tk.Frame(self.master, padx=8, pady=8)
#         self.frame_option = tk.Frame(self.master, padx=8, pady=8)
#         self.frame_action = tk.Frame(self.master, padx=8, pady=8)

#         self.label_file = tk.Label(self.frame_file, text='設定ファイル')
#         self.text_file = tk.Entry(self.frame_file, width=50, textvariable='', state='readonly')
#         self.button_file = tk.Button(self.frame_file, text='選択', command=self.say_hi)

#         self.label_file.pack(side='left')
#         self.text_file.pack(side='left')
#         self.button_file.pack(side='left')

#         self.frame_file.pack(side='top')
#         self.frame_select.pack(side='top')
#         self.frame_option.pack(side='top')
#         self.frame_action.pack(side='top')

#         self.hi_there = tk.Button(self)
#         self.hi_there["text"] = "Hello World\n(click me)"
#         self.hi_there["command"] = self.say_hi
#         self.hi_there.pack(side="top")

#         self.quit = tk.Button(self, text="QUIT", fg="red",
#                               command=self.master.destroy)
#         self.quit.pack(side="bottom")

#     def say_hi(self):
#         print("hi there, everyone!")

# def create_tmp_file(filename: str, encoding=ENC) -> str:
#     enc = encoding
#     if os.path.isabs(filename) is False:
#         filename = os.path.join(get_pwd(), filename)
#     if os.path.exists(filename):
#         try:
#             with open(filename, 'rb') as f:
#                 enc = encoding_detector(f.read())
#                 if enc is None:
#                     enc = encoding
#             with codecs.open(filename, 'r', enc) as f:
#                 data = f.read()
#                 out_filename = '{0}.{1}'.format(filename, str(uuid.uuid4()))
#                 with codecs.open(out_filename, 'w', enc) as fw:
#                     data = data.replace('%', '%%')
#                     fw.write(data)
#                     return out_filename
#         except BaseException:
#             return None
#     return None
