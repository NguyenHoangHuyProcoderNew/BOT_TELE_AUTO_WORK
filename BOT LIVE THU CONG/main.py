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
API_TOKEN = '7329003333:AAF7GhjivbGnk0jSGE8XfefFh_-shHAFsGc'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

chat_id = '5634845912' # ID CỦA NGƯỜI DÙNG

# IMPORT CHỨC NĂNG MỞ LIVE TÀI KHOẢN MEME LỎ
from molive.molive_memelo import main_molive_memelo

########################### BẮT ĐẦU CÁC CHỨC NĂNG CỦA BOT ###########################

print(f"============= | KHỞI ĐỘNG BOT LIVESTREAM THÀNH CÔNG | =============")

# CHỨC NĂNG MỞ LIVE TÀI KHOẢN MEME LỎ
@bot.message_handler(commands=['molive_memelo'])
def molive_memelo(message):
    main_molive_memelo(message)

########################################################
####################### CHẠY BOT #######################
########################################################
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception("LỖI")
        time.sleep(5)