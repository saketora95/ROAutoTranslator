# coding=utf-8

import datetime
import os
from time import sleep
import tkinter as tk
import compare_process
import logging
from tkinter import messagebox
import pyperclip

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

TEST_MODE = 1
TEST_TEXT = '야수의 가죽 신발 [1]\n월야화의 가죽신을 모티브로 제작된 가죽 신발.\n\nMHP + 1500, MSP + 150.\n7제련 시, MATK + 3%.\n9제련 시, MATK + 5% 추가 증가, S.MATK + 5.\n11제련 시, 고정 캐스팅 0.8초 감소, 변동 캐스팅 10% 감소.\n\n월야화 카드와 함께 장착 시, 고정 캐스팅 0.2초 감소, S.MATK + 15.\n봉인된 월야화 카드와 함께 장착 시, 고정 캐스팅 0.2초 감소.\n분노한 월야화 카드와 함께 장착 시, 신발 3제련당 모든 속성 마법 데미지 4%씩 증가.\n\n[등급별 추가 옵션]\n[D등급] RES + 30, MRES + 30.\n[C등급] 모든 크기 적에게 주는 마법 데미지 15% 증가.\n[B등급] SPL + 3.\n[A등급] S.MATK + 7.\n계열 : 신발 방어 : 15\n무게 : 60\n방어구 레벨 : 2\n요구 레벨 : 200\n장착 : 전 직업\n'

class Translator(tk.Tk):
    
    # Initial
    def __init__(self, current_date_string, log_path, compare_list_path):

        # Basic initial
        super().__init__()
        self.resizable(0, 0)
        self.protocol('WM_DELETE_WINDOW', self.close_window)

        # Log file
        self.initial_log_file(
            'Log ' + current_date_string + '.txt',
            log_path
        )
        self.LogFile.info('初始化...')

        # Compare list
        self.CompareFilePath = compare_list_path
        self.CompareDict = compare_process.read_compare_file(self.CompareFilePath)
        self.LogFile.info('比對文件讀取: {0}'.format(self.CompareDict))

        # UI initial
        self.initial_user_interface()

        # Test mode
        self.test_mode()

        self.LogFile.info('初始化完成.')

    def initial_log_file(self, file_name, log_path):
        logging.basicConfig(
            level=logging.INFO,
            filemode='a',
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.LogFile = logging.getLogger(file_name)
        self.LogFile.setLevel(logging.INFO)
        self.LogHandler = logging.FileHandler(
            log_path + file_name,
            'a',
            encoding='utf-8'
        )
        self.LogHandler.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
        )

    def initial_user_interface(self):
        # Window
        self.geometry('{0}x{1}+{2}+{3}'.format(
            WINDOW_WIDTH,
            WINDOW_HEIGHT,
            int((self.winfo_screenwidth() - WINDOW_WIDTH) / 2),
            int((self.winfo_screenheight() - WINDOW_HEIGHT) / 2)
        ))
        self.title('RO Auto Translator')

        # Text input and output
        self.TextInput = tk.Text(self)
        self.TextInput.place(x=10, y=40, width=240, height=310)

        self.TextOutput = tk.Text(self)
        self.TextOutput.place(x=350, y=40, width=240, height=310)

        # Label
        self.Label_KR = tk.Label(self, text='韓文原文')
        self.Label_KR.place(x=10, y=10, width=240, height=30)
        self.Label_KR = tk.Label(self, text='轉換結果')
        self.Label_KR.place(x=350, y=10, width=240, height=30)

        # Button
        self.Btn_Reload = tk.Button(self, text='重新讀取', command=self.btn_reload)
        self.Btn_Reload.place(x=260, y=10, width=80, height=30)

        self.Btn_Translate = tk.Button(self, text='→ 轉換 →', command=self.btn_translate)
        self.Btn_Translate.place(x=260, y=185, width=80, height=30)

        self.Btn_Paste = tk.Button(self, text='貼上', command=self.btn_paste)
        self.Btn_Paste.place(x=10, y=360, width=80, height=30)

        self.Btn_CleanAndPaste = tk.Button(self, text='清空並貼上', command=self.btn_clean_and_paste)
        self.Btn_CleanAndPaste.place(x=100, y=360, width=150, height=30)

        self.Btn_Copy = tk.Button(self, text='複製', command=self.btn_copy)
        self.Btn_Copy.place(x=350, y=360, width=80, height=30)

    def test_mode(self):
        if TEST_MODE == 1:
            self.TextInput.insert(1.0, TEST_TEXT)
            self.LogFile.info('啟用測試模式，在 TextInput 自動追加文字: \n' + TEST_TEXT)

    def close_window(self):
        self.LogFile.info('使用者點選關閉按鈕...')
        if messagebox.askyesno('操作詢問', '您確定要關掉 ROAutoTranslator 了嗎？'):
            self.LogFile.info('使用者確認關閉程式.')
            sleep(0.5)
            self.destroy()
        
        else:
            self.LogFile.info('使用者取消關閉程式.')

    def btn_reload(self):
        self.CompareDict = compare_process.read_compare_file(self.CompareFilePath)
        self.LogFile.info('比對文件讀取: \n{0}'.format(self.CompareDict))

    def btn_translate(self):
        self.TextOutput.delete(1.0, 'end')
        self.LogFile.info('清空 TextOutput 文字')

        target = self.TextInput.get(1.0, 'end')
        self.LogFile.info('轉換目標: \n' + target)

        result = compare_process.compare_string(target, self.CompareDict)
        self.LogFile.info('轉換結果: \n' + result)

        self.TextOutput.insert(1.0, result)

    def btn_paste(self):
        self.TextInput.insert('end', pyperclip.paste())
        self.LogFile.info('貼上文字到 TextInput: ' + pyperclip.paste())

    def btn_clean_and_paste(self):
        self.TextInput.delete(1.0, 'end')
        self.LogFile.info('清空 TextInput 文字')
        self.TextInput.insert(1.0, pyperclip.paste())
        self.LogFile.info('貼上文字到 TextInput: \n' + pyperclip.paste())

    def btn_copy(self):
        copy_data = self.TextOutput.get(1.0, 'end')
        pyperclip.copy(copy_data)
        self.LogFile.info('複製 TextOutput 文字: \n' + copy_data)

