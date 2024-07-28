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
from colorama import init, Fore

# KHAI BÁO APT TOKEN BOT TELEGRAM
API_TOKEN = '7371036517:AAEB8PtQRtSrvDOxQUUW2su7ObGso6ltq8w'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

# CẤU HÌNH WEBDRIVER
chromedriver_path = r'D:\\BOT_TELE_AUTO_WORK\\BOT LIVE THU CONG\\chrome_driver\\chromedriver.exe'

options = Options()
options.add_argument('--log-level=3')  # Vô hiệu hóa thông báo của Selenium
options.add_argument('--user-data-dir=D:\\BOT_TELE_AUTO_WORK\\BOT LIVE THU CONG\\du lieu trinh duyet')

service = Service(chromedriver_path)
service_log_path = os.path.devnull
service = Service(chromedriver_path, service_log_path=service_log_path)

# user_id = '5634845912' # ID CỦA NGƯỜI DÙNG

# HÀM ĐẾM NGƯỢC SỐ PHÚT
def countdown(minutes):
    total_seconds = minutes * 60
    for i in range(total_seconds, 0, -1):
        minutes, seconds = divmod(i, 60)
        print(f"Còn {minutes} phút {seconds} giây nữa sẽ tiến hành kiểm tra phiên live.")
        time.sleep(1)
    print("Đếm ngược hoàn tất, tiến hành kiểm tra trạng thái phiên live")

# CHỈ GỬI TIN NHẮN CHO NGƯỜI DÙNG MÀ KHÔNG IN RA MÀN HÌNH
def bot_reply(user_id, message):
    # Gửi tin nhắn đến người dùng
    bot.send_message(user_id, message)    

# IN VĂN BẢN THÀNH MÀU ĐỎ
def print_red(text):
    red_color_code = "\033[91m"
    reset_code = "\033[0m"
    print(f"{red_color_code}[*] {text}{reset_code}")   

# IN VĂN BẢN THÀNH MÀU VÀNG
def print_yellow(text):
    yellow_color_code = "\033[93m"
    reset_code = "\033[0m"
    print(f"{yellow_color_code}[*] {text}{reset_code}")  

# IN VĂN BẢN THÀNH MÀU XANH LÁ CÂY
def print_green(text):
    green_color_code = "\033[92m"
    reset_code = "\033[0m"
    print(f"{green_color_code}[*] {text}{reset_code}")

# IN RA RA MÀN HÌNH MÀU ĐỎ VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
def print_red_and_send_message(user_id, message):
    # Gửi tin nhắn đến người dùng
    bot.send_message(user_id, message)
    # In ra màn hình với màu đỏ
    print(Fore.RED + '[*] ' + message + Fore.RESET)

# IN RA MÀN HÌNH MÀU VÀNG VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
def print_yellow_and_send_message(chat_id, message):
    # Gửi tin nhắn đến người dùng
    bot.send_message(chat_id, message)
    # In ra màn hình với ký tự đầu là [*] và màu vàng
    print(Fore.YELLOW + '[*] ' + message + Fore.RESET)    

# IN RA MÀN HÌNH MÀU XANH LÁ CÂY VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
def print_green_and_send_message(chat_id, message):
    # Gửi tin nhắn đến người dùng
    bot.send_message(chat_id, message)
    # In ra màn hình với ký tự đầu là [*] và màu xanh lác cây
    print(Fore.GREEN + '[*] ' + message + Fore.RESET)    

# CHỨC NĂNG KHỞI ĐỘNG LẠI BOT
def handle_restart(message):
    restart_bot(message)

# Hàm để restart bot
def restart_bot(message):
    driver = webdriver.Chrome(service=service, options=options)
    bot.reply_to(message, "Khởi động lại bot thành công")
    driver.quit()  # Đóng trình duyệt Selenium trước khi restart
    os.execv(sys.executable, ['python'] + sys.argv)    