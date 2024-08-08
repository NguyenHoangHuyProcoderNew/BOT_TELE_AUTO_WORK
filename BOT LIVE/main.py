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
from selenium.common.exceptions import TimeoutException
from telebot import types
# GỌI CÁC CHỨC NĂNG CỦA FILE DYLIB
from dylib import dylib

# KHAI BÁO API TOKEN BOT TELEGRAM
API_TOKEN = '7371036517:AAEB8PtQRtSrvDOxQUUW2su7ObGso6ltq8w'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

# CÁC CHỨC NĂNG IN RA MÀN HÌNH
from print_logger.print_logger import log_info, log_warning, log_error, log_success

# Nhập chức năng bot phản hồi lại người dùng
from dylib.dylib import bot_reply

from dylib.dylib import user_id
from dylib.dylib import username

log_info(f"KHỞI ĐỘNG BOT LIVESTREAM THÀNH CÔNG - ĐANG CHỜ LỆNH TỪ NGƯỜI DÙNG...")

# CHỨC NĂNG START
@bot.message_handler(commands=['start'])
def start(message):   
    log_info(f"Người dùng {username} - ID: {user_id} đã sử dụng lệnh /start")
    # TẠO NÚT CHO CHỨC NĂNG START
    button_start = telebot.types.ReplyKeyboardMarkup(True)
    button_start.add("Đổi IP").add("Mở live").add("Tắt live")
    text = "CHÀO MỪNG BẠN QUAY LẠI BOT, CHÚC BẠN NGÀY MỚI VUI VẺ"
    bot.send_message(message.chat.id, text, reply_markup=button_start)

# ĐỔI IP
@bot.message_handler(func=lambda message: message.text in ["Đổi IP", "Có, tiếp tục đổi IP"])
def handle_doiip(message):
    log_info(f"Người dùng {username} - ID: {user_id} đã chọn đổi IP từ menu chính")
    # GỌI HÀM ĐỔI IP TRONG FILE DOIIP.PY TRONG FOLDER DOIIP
    from doiip.doiip import ask_select_account_doiip
    from doiip.doiip import doiip_main
    ask_select_account_doiip(message)
    bot.register_next_step_handler(message, doiip_main)

# CHỨC NĂNG TẮT LIVE
@bot.message_handler(func=lambda message: message.text == "Tắt live")
def handle_tatlive(message):
    log_info(f"Người dùng {username} - ID: {user_id} đã chọn Tắt live từ menu chính")
    from tatlive.tatlive import xacnhan_tatlive
    from tatlive.tatlive import main_tatlive

    xacnhan_tatlive(message)
    bot.register_next_step_handler(message, main_tatlive)

# CHỨC NĂNG MỞ LIVE
@bot.message_handler(func=lambda message: message.text == "Mở live")
def select_molive(message):
    log_info(f"Người dùng {username} - ID: {user_id} đã chọn Mở live từ menu chính")
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

### Trở lại menu chính ###
@bot.message_handler(func=lambda message: message.text in ["Trở lại menu chính", "Không, trở về menu chính"])
def handle_back_home(message):
    # Gọi hàm xử lý việc trở lại menu chính
    log_info("Người dùng đã chọn Trở Lại Menu Chính")
    back_home(message)

# Hàm xử lý việc trở lại menu chính
def back_home(message):
    text = "VUI LÒNG CHỌN 👇"
    # TẠO NÚT CHO CHỨC NĂNG TRỞ VỀ MENU CHÍNH
    button_backhome = telebot.types.ReplyKeyboardMarkup(True)
    button_backhome.add("Đổi IP").add("Mở live").add("Tắt live").add("Check view")
    bot.send_message(message.chat.id, text, reply_markup=button_backhome)

# Check view
@bot.message_handler(func=lambda message: message.text == "Check view")
def checkview(message):
    from checkview.checkview import ask_select_account_checkview
    from checkview.checkview import checkview_main

    ask_select_account_checkview(message)
    bot.register_next_step_handler(message, checkview_main)

########################################################
####################### CHẠY BOT #######################
########################################################
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception("LỖI")
        time.sleep(5)