# !/usr/bin/python
# -*- coding: utf-8 -*-
# ===== サクラエディタ・タイプ別設定一括コピープログラム
"""サクラエディタ・タイプ別設定一括コピープログラム

サクラエディタに定義されているすべての「タイプ別設定」を、
選択した「タイプ別設定」の値に変更するプログラムです。
"""

__author__ = 'Iori Tsukuyomi'
__credit__ = 'Copyright (C) 2022 Iori Tsukuyomi All Rights Reserved.'
__date__ = '2022/01/01'
__version__ = '1.0.0'

import codecs
import configparser
import imp
import os
import sys

# ----- 定数宣言
ENC = 'utf_8_sig'
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
    status = (
        hasattr(
            sys,
            'frozen') or hasattr(
            sys,
            'importers') or imp.is_frozen('__main__'))
    if status:
        return os.path.abspath(os.path.dirname(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


# ----- iniファイルの内容を辞書として取得
def load_inifile(filename: str, encoding=ENC) -> configparser:
    if os.path.isabs(filename) is False:
        filename = os.path.join(get_pwd(), filename)
    if os.path.exists(filename):
        # try:
        with open(filename, 'rb') as f:
            encoding = encoding_detector(f.read())
            if encoding is None:
                encoding = ENC
        cp = configparser.ConfigParser(empty_lines_in_values=True)
        cp.BasicInterpolation = None
        cp.optionxform = str
        cp.read(filename, encoding)
        return cp
        # except BaseException:
        #     return None
    return None


# ----- 辞書の内容をiniファイルに書き出し
def save_inifile(filename: str, cp: configparser, encoding=ENC) -> bool:
    if os.path.isabs(filename) is False:
        filename = os.path.join(get_pwd(), filename)
    if os.path.exists(filename):
        try:
            with codecs.open(filename, 'w', encoding=encoding) as f:
                cp.write(f)
            return True
        except BaseException:
            return False
    return False


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
def save_textfile(data_list, filename, encoding=ENC, newline='\n'):
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


# ----- 単体実行時の処理
if __name__ == '__main__':

    # param = load_inifile(create_tmp_file('C:/sakura/sakura.ini'))
    cp = load_inifile('C:/sakura/sakura.ini')
    # save_inifile('C:/sakura/sakura-mod.ini', cp)
    # print(get_setting_list(cp))
    print(get_item_list('C:/sakura/sakura.ini', 13))
    # print(param)


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
