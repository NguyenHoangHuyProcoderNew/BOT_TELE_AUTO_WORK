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

chat_id = '5634845912' # ID CỦA NGƯỜI DÙNG

########################### BẮT ĐẦU CÁC CHỨC NĂNG CỦA BOT ###########################
print(f"============= | KHỞI ĐỘNG BOT TẠO KEY THÀNH CÔNG | =============")

# CHỨC NĂNG TẠO KEY IOS USER
from IOS.ios_user import ask_user_timekey_ios_user
from IOS.ios_user import main_create_key_ios_user
@bot.message_handler(commands=['ios_user'])
def ios_user(message):
    ask_user_timekey_ios_user(message)
    bot.register_next_step_handler(message, main_create_key_ios_user)

# CHỨC NĂNG TẠO KEY IOS VIP
from IOS.ios_vip import main_ios_vip
from IOS.ios_vip import timekey_ios_vip
@bot.message_handler(commands=['ios_vip'])
def ios_vip(message):
    main_ios_vip(message)
    bot.register_next_step_handler(message, timekey_ios_vip)

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