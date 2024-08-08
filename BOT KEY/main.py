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

# KHAI BÁO APT TOKEN BOT TELEGRAM
API_TOKEN = '6555297922:AAF7DFvu9c-gi10-wBtwa_3jKa3TeyInNQ8'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

# CÁC CHỨC NĂNG IN RA MÀN HÌNH
from print_logger.print_logger import log_info, log_warning, log_error, log_success

# Nhập chức năng bot phản hồi lại người dùng
from dylib.dylib import bot_reply

from dylib.dylib import user_id
from dylib.dylib import username

########################### BẮT ĐẦU CÁC CHỨC NĂNG CỦA BOT ###########################
log_info("Khởi động bot tạo key thành công, đang đợi lệnh từ người dùng...")

# Tạo key IOS server USER
@bot.message_handler(commands=['ios_user'])
def create_key_ios_user(message):
    from IOS.ios_user import ask_user_timekey_ios_user
    from IOS.ios_user import main_create_key_ios_user
    log_info(f"Người dùng {username} đã sử dụng lệnh /ios_user")
    ask_user_timekey_ios_user(message)
    bot.register_next_step_handler(message, main_create_key_ios_user)

# CHỨC NĂNG TẠO KEY IOS VIP
from IOS.ios_vip import ask_user_timekey_ios_vip
from IOS.ios_vip import main_create_key_ios_vip
@bot.message_handler(commands=['ios_vip'])
def ios_vip(message):
    ask_user_timekey_ios_vip(message)
    bot.register_next_step_handler(message, main_create_key_ios_vip)

# CHỨC NĂNG TẠO KEY ANDROID
from ANDROID.android import ask_user_timekey_android
from ANDROID.android import main_create_key_android
@bot.message_handler(commands=['android'])
def android(message):
    ask_user_timekey_android(message)
    bot.register_next_step_handler(message, main_create_key_android)
    
########################################################
####################### CHẠY BOT #######################
########################################################
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception("LỖI")
        time.sleep(5)