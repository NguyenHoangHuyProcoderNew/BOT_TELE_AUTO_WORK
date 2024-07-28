# IMPORT CÁC THƯ VIỆN CẦN THIẾT
import os
import time
import logging
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import telebot
import sys
import pyperclip
from selenium.common.exceptions import NoSuchElementException
logging.basicConfig(level=logging.CRITICAL)  # Chỉ in thông báo lỗi nghiêm trọng
import datetime
now = datetime.datetime.now()
from selenium.common.exceptions import TimeoutException
from telebot import types
from dylib import dylib

# KHAI BÁO APT TOKEN BOT TELEGRAM
API_TOKEN = '7371036517:AAEB8PtQRtSrvDOxQUUW2su7ObGso6ltq8w'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

user_id = '5634845912' # ID CỦA NGƯỜI DÙNG

########################### BẮT ĐẦU CÁC CHỨC NĂNG CỦA BOT ###########################
print(f"============= | KHỞI ĐỘNG BOT LIVESTREAM THÀNH CÔNG | =============")

# CHỨC NĂNG /START
start = telebot.types.ReplyKeyboardMarkup(True).add("Đổi IP").add("Mở live").add("Tắt live")
@bot.message_handler(commands=['start'])
def handle_start(message):
    text = "CHÀO MỪNG BẠN QUAY LẠI BOT, CHÚC BẠN NGÀY MỚI VUI VẺ"
    bot.send_message(message.chat.id, text, reply_markup=start)

# CHỨC NĂNG ĐỔI IP
@bot.message_handler(func=lambda message: message.text == "Đổi IP")
def handle_doiip(message):
    from doiip.doiip import ask_select_account_doiip
    from doiip.doiip import doiip_main
    ask_select_account_doiip(message)
    bot.register_next_step_handler(message, doiip_main)

# CHỨC NĂNG TẮT LIVE
@bot.message_handler(func=lambda message: message.text == "Tắt live")
def handle_tatlive(message):
    from tatlive.tatlive import xacnhan_tatlive
    from tatlive.tatlive import main_tatlive

    xacnhan_tatlive(message)
    bot.register_next_step_handler(message, main_tatlive)

# CHỨC NĂNG MỞ LIVE
@bot.message_handler(func=lambda message: message.text == "Mở live")
def select_molive(message):
    select_molive_button = types.ReplyKeyboardMarkup(True).add('Nick Chính Văn Bảo').add('Nick Phụ LBH').add("Nick Meme Lỏ").add('Trở lại menu chính')
    text = "Vui lòng chọn tài khoản cần mở live"
    bot.send_message(message.chat.id, text, reply_markup=select_molive_button)

# MỞ LIVE VĂN BẢO
@bot.message_handler(func=lambda message: message.text == "Nick Chính Văn Bảo")
def handle_molivevanbao(message):
    from molive.molive_vanbao import ask_source_live_vanbao, main_molive_vanbao
    ask_source_live_vanbao(message)
    bot.register_next_step_handler(message, main_molive_vanbao)

# MỞ LIVE NICK PHỤ LBH
@bot.message_handler(func=lambda message: message.text == "Nick Phụ LBH")
def handle_molivenickphulbh(message):
    from molive.molive_nickphulbh import ask_source_live_nickphulbh, main_molive_nickphulbh
    ask_source_live_nickphulbh(message)
    bot.register_next_step_handler(message, main_molive_nickphulbh)

# MỞ LIVE MEME LỎ
@bot.message_handler(func=lambda message: message.text == "Nick Meme Lỏ")
def handle_molivenickphulbh(message):
    from molive.molive_memelo import ask_source_live_memelo, main_molive_memelo
    ask_source_live_memelo(message)
    bot.register_next_step_handler(message, main_molive_memelo)   

# TRỞ LẠI MENU CHÍNH
@bot.message_handler(func=lambda message: message.text == "Trở lại menu chính")
def handle_back_home(message):
    back_home(message)

def back_home(message):
    text = "VUI LÒNG CHỌN 👇"
    bot.send_message(message.chat.id, text, reply_markup=start)

########################################################
####################### CHẠY BOT #######################
########################################################
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception("LỖI")
        time.sleep(5)