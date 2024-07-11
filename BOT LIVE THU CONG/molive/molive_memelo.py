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
# CẤU HÌNH LOGGING
logging.basicConfig(level=logging.CRITICAL)  # Chỉ in thông báo lỗi nghiêm trọng
import datetime
now = datetime.datetime.now()
from selenium.common.exceptions import TimeoutException
from nguonlive.linknguon import linknguon
from dylib import dylib

# CẤU HÌNH WEBDRIVER
chromedriver_path = r'C:\\Users\\Administrator\\Desktop\\BOT_TELE_AUTO_WORK\\BOT LIVE THU CONG\\chrome_driver\\chromedriver.exe'

options = Options()
options.add_argument('--log-level=3')  # Vô hiệu hóa thông báo của Selenium
options.add_argument('--user-data-dir=C:\\Users\\Administrator\\Desktop\\BOT_TELE_AUTO_WORK\\BOT LIVE THU CONG\\du lieu trinh duyet')

service = Service(chromedriver_path)
service_log_path = os.path.devnull
service = Service(chromedriver_path, service_log_path=service_log_path)

# KHAI BÁO APT TOKEN BOT TELEGRAM
API_TOKEN = '7329003333:AAF7GhjivbGnk0jSGE8XfefFh_-shHAFsGc'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

chat_id = '5634845912' # ID CỦA NGƯỜI DÙNG

# THÔNG TIN TÀI KHOẢN LIVE
ten_tai_khoan = "MEME LỎ"
id_tiktok = "meme.l810"

############################ CHỨC NĂNG CHÍNH ##########################
def main_molive_memelo(message):
    print(f"============= | MỞ LIVE TÀI KHOẢN {ten_tai_khoan} | =============")

    # IN RA MÀN HÌNH
    dylib.print_yellow("Khởi tạo web driver")
     # Khởi tạo webdriver
    driver = webdriver.Chrome(service=service, options=options)
    
    # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
    dylib.print_yellow_and_send_message(chat_id, f"Tiến hành mở livestream tài khoản {ten_tai_khoan}")

    sleep(1)

    # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
    dylib.print_green(chat_id, "Mở website livestream")

    # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
    driver.get('https://autolive.me/tiktok')

    sleep(1000)