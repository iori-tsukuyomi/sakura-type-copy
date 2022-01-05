# !/usr/bin/python
# -*- coding: utf-8 -*-
# ===== サクラエディタ・タイプ別設定一括コピー
"""サクラエディタ・タイプ別設定一括コピー

サクラエディタに定義されているすべての「タイプ別設定」を、
選択した「タイプ別設定」の値に変更するプログラムです。
"""

__author__ = 'Iori Tsukuyomi'
__credit__ = 'Copyright (C) 2022 Iori Tsukuyomi All Rights Reserved.'
__date__ = '2022/01/05'
__version__ = '1.0.0'

import codecs
import configparser
import ctypes
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox

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


def get_pwd() -> str:
    if getattr(sys, "frozen", False):
        return os.path.abspath(os.path.dirname(sys.executable))
    else:
        return os.path.dirname(os.path.abspath(__file__))


def load_inifile(filename: str, encoding=ENC) -> configparser:
    try:
        cp = configparser.ConfigParser(empty_lines_in_values=True)
        cp.BasicInterpolation = None
        cp.optionxform = str
        cp.read(filename, encoding)
        return cp
    except BaseException:
        return None


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
    if datas:
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
    else:
        return None


def set_items(filename: str, item_list: dict, encoding=ENC) -> dict:
    flag = 0
    datas = load_textfile(filename, encoding=encoding)
    if datas:
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
    else:
        return None


class Application():
    def __init__(self, top=None):
        self.style = ttk.Style()
        self.style.theme_use('winnative')
        top.geometry('580x130+150+150')
        top.resizable(0, 0)
        top.title('サクラエディタ・タイプ別設定一括コピー')

        self.top = top
        self.combobox = tk.StringVar()

        self.filename = ''
        self.encoding = ENC
        self.cp = None
        self.type_list = None

        self.TLabel1 = ttk.Label(self.top)
        self.TLabel1.place(x=10, y=10, height=28, width=100)
        self.TLabel1.configure(relief='flat')
        self.TLabel1.configure(anchor='w')
        self.TLabel1.configure(justify='left')
        self.TLabel1.configure(text='設定ファイル名')
        self.TLabel1.configure(compound='left')

        self.entry_file = ttk.Entry(self.top)
        self.entry_file.place(x=110, y=10, height=28, width=380)
        self.entry_file.configure(state='readonly')
        self.entry_file.configure(takefocus='')
        self.entry_file.configure(cursor='fleur')

        self.TLabel2 = ttk.Label(self.top)
        self.TLabel2.place(x=10, y=50, height=28, width=100)
        self.TLabel2.configure(relief='flat')
        self.TLabel2.configure(anchor='w')
        self.TLabel2.configure(justify='left')
        self.TLabel2.configure(text='コピー元タイプ')
        self.TLabel2.configure(compound='left')

        self.button_select = ttk.Button(self.top)
        self.button_select.place(x=500, y=8, height=30, width=76)
        self.button_select.configure(takefocus='')
        self.button_select.configure(text='選択')
        self.button_select.configure(compound='left')
        self.button_select.configure(command=self.get_filename)

        self.combobox_type = ttk.Combobox(self.top)
        self.combobox_type.place(x=110, y=50, height=28, width=380)
        self.combobox_type.configure(textvariable=self.combobox)
        self.combobox_type.configure(takefocus='')

        self.button_exec = ttk.Button(self.top)
        self.button_exec.place(x=420, y=88, height=30, width=76)
        self.button_exec.configure(takefocus='')
        self.button_exec.configure(text='実行')
        self.button_exec.configure(compound='left')
        self.button_exec.configure(command=self.set_types)

        self.button_quit = ttk.Button(self.top)
        self.button_quit.place(x=500, y=88, height=30, width=76)
        self.button_quit.configure(takefocus='')
        self.button_quit.configure(text='終了')
        self.button_quit.configure(compound='left')
        self.button_quit.configure(command=self.quit)

    def get_filename(self):
        self.filename = filedialog.askopenfilename(
            filetypes=[('設定ファイル', '*.ini')])
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
        # Check Sakura-Editor version.
        ver = False
        try:
            ver = self.cp['Other']['szVersion']
            if ver == '2.4.1.2849':
                ver = True
        except BaseException:
            pass
        if ver is False:
            messagebox.showerror(TITLE, 'バージョン「2.4.1.2849」の設定ファイルを選択してください。')
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

    def set_types(self):
        if self.combobox.get() == '':
            messagebox.showwarning(TITLE, 'コピー元タイプを選択してください。')
            return False
        ret = messagebox.askokcancel(
            TITLE, 'タイプ「{0}」の色指定と縦線桁指定をすべてのタイプに適用します。よろしいですか?'.format(
                self.combobox.get()))
        if ret:
            item_list = get_item_list(
                self.filename, self.type_list[self.combobox.get()])
            if item_list:
                datas = set_items(
                    self.filename,
                    item_list,
                    encoding=self.encoding)
                if datas:
                    save_textfile(
                        datas,
                        self.filename,
                        encoding=self.encoding)
                    messagebox.showinfo(TITLE, '正常に適用されました。アプリケーションを終了してください。')
                else:
                    messagebox.showerror(TITLE, 'タイプの適用に失敗しました。処理を中断しました。')
                    return False
            else:
                messagebox.showerror(
                    TITLE, '設定項目が取得できませんでした。正しいファイルを選択してください。')
                return False
        return True

    def quit(self):
        self.top.destroy()


# ----- Main
if __name__ == '__main__':
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
    except BaseException:
        pass
    root = tk.Tk()
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(data=ICON_DATA))
    app = Application(top=root)
    root.mainloop()
