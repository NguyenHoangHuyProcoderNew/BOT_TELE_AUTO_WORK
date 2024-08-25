# Import các thư viện cần thiết
import os
from telnetlib import DM
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
import datetime
now = datetime.datetime.now()
from selenium.common.exceptions import TimeoutException

# Khai báo Token của BOT
API_TOKEN = '7371036517:AAEB8PtQRtSrvDOxQUUW2su7ObGso6ltq8w' # Token của BOT
bot = telebot.TeleBot(API_TOKEN)

# Nhập moudle in các log ra màn hình
from print_logger.print_logger import log_info, log_warning, log_error, log_success

# Nhập moudle bot phản hồi lại người dùng
from dylib.dylib import bot_reply

# Nhập id và user name của người dùng
from dylib.dylib import user_id
from dylib.dylib import username

########## BẮT ĐẦU MÃ CHO CÁC CHỨC NĂNG CỦA BOT #######
log_success("Khởi động bot tạo key thành công.")

# Tạo key IOS server USER
@bot.message_handler(commands=['ios_user'])
def taokey_ios_user(message):
    # Import các moudle tạo key ios_user
    from IOS.ios_user import nhap_thoigian_key
    from IOS.ios_user import xuly_taokey_ios_user

    nhap_thoigian_key(message)
    bot.register_next_step_handler(message, xuly_taokey_ios_user)

# Tạo key IOS server VIP
@bot.message_handler(commands=['ios_vip'])
def ios_vip(message):
    # Import các moudle tạo key ios_vip
    from IOS.ios_vip import nhap_thoigian_key
    from IOS.ios_vip import xuly_taokey_ios_vip
    nhap_thoigian_key(message)
    bot.register_next_step_handler(message, xuly_taokey_ios_vip)

# Tạo key ANDROID
@bot.message_handler(commands=['android'])
def taokey_android(message):
    # Nhập các moudle thực hiện việc tạo key
    from ANDROID.android import nhap_thoigian_key
    from ANDROID.android import xuly_taokey_android

    log_info(f"Người dùng đã yêu cầu tạo key android")
    nhap_thoigian_key(message)
    bot.register_next_step_handler(message, xuly_taokey_android)
    
########################################################
####################### CHẠY BOT #######################
########################################################
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception("LỖI")
        time.sleep(5)
