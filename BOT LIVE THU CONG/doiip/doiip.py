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
from colorama import Fore, Style, init

# NHẬP FILE DYLIB CHỨA CÁC HÀM QUAN TRỌNG
from dylib import dylib

# CẤU HÌNH WEBDRIVER
chromedriver_path = r'D:\\BOT_TELE_AUTO_WORK\\BOT LIVE THU CONG\\chrome_driver\\chromedriver.exe'

options = Options()
options.add_argument('--log-level=3')  # Vô hiệu hóa thông báo của Selenium
options.add_argument('--user-data-dir=D:\\BOT_TELE_AUTO_WORK\\BOT LIVE THU CONG\\du lieu trinh duyet')

service = Service(chromedriver_path)
service_log_path = os.path.devnull
service = Service(chromedriver_path, service_log_path=service_log_path)

# KHAI BÁO APT TOKEN BOT TELEGRAM
API_TOKEN = '7329003333:AAF7GhjivbGnk0jSGE8XfefFh_-shHAFsGc'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

user_id = '5634845912' # ID CỦA NGƯỜI DÙNG

ip = None
device = None

############################ CHỨC NĂNG CHÍNH ##########################
def ask_select_account_doiip(message):
    # GỬI TIN NHẮN CHO NGƯỜI DÙNG
    dylib.bot_reply(user_id, "THỰC THI LỆNH THÀNH CÔNG")

    # IN RA MÀN HÌNH
    print(f"\n============= | YÊU CẦU NGƯỜI DÙNG CHỌN TÀI KHOẢN CẦN ĐỔI IP | =============")

    # YÊU CẦU NGƯỜI DÙNH CHỌN TÀI KHOẢN
    dylib.bot_reply(user_id, "Đang đợi người dùng chọn tài khoản cần đổi IP..."); dylib.bot_reply(user_id, "Vui lòng chọn tài khoản cần đổi IP\n1. Văn Bảo\n2.Nick phụ LBH\n3.Meme Lỏ\nNhập số 1-3 để chọn tài khoản")

    bot.register_next_step_handler(message, doiip)

def doiip(message):
    global ip
    global device

    # NHẬN DỮ LIỆU MÀ NGƯỜI DÙNG NHẬP
    user_message_select = message.text.strip()

    if user_message_select == "1":
        ip = "ip-22680"
        device = "renew-22680"
    elif user_message_select == "2":
        ip = "ip-22679"
        device = "renew-22679"
    elif user_message_select == "3":
        ip = ""


    # KHỞI TẠO WEB DRIVER
    driver = webdriver.Chrome(service=service, options=options)

    # IN RA MÀN HÌNH
    dylib.print_red("KHỞI TẠO WEB DRIVER\n")

    # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
    dylib.print_green_and_send_message(user_id,"Truy cập website livestream")

    # MỞ WEB LIVESTREAM
    driver.get('https://autolive.me/tiktok')

    # KIỂM TRA XEM TRANG WEB LOAD XONG CHƯA
    try:
        # IN RA MÀN HÌNH
        dylib.print_green_and_send_message(user_id, "Đang load website...")

        # ĐỢI PHẦN TỬ CỦA WEB XUẤT HIỆN
        # SAU KHI PHẦN TỬ XUẤT HIỆN => KẾT LUẬN WEB ĐÃ LOAD XONG
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))

        # IN VÀ GỬI TIN NHẮN
        dylib.print_yellow_and_send_message(user_id, "Truy cập website livestream thành công")
    except TimeoutError:
        # IN VÀ GỬI TIN NHẮN
        dylib.print_green_and_send_message(user_id, "Truy cập website livestream thất bại")

        # ĐÓNG CHROME
        driver.quit()

        # KẾT THÚC TIẾN TRÌNH
        return

    # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
    dylib.print_red_and_send_message(user_id, "TIẾN HÀNH ĐỔI IP")

    # IN RA MÀN HÌNH
    dylib.print_red("Click vào nút Thêm TK bằng Web")

    # CHECK TÊN TÀI KHOẢN NICK PHU LBH
    checkname_nickphulbh = driver.find_element(By.CSS_SELECTOR, "#table-tiktok-account > tbody > tr:nth-child(2) > td.text-left")
    name_nickphulbh = checkname_nickphulbh.text

    # GỬI TIN NHẮN CHO NGƯỜI DÙNG VÀ IN RA MÀN HÌNH
    dylib.print_green_and_send_message(user_id, f"Đổi IP cho tài khoản {name_nickphulbh}")

    div > div.notifyjs-container > div > div.text-wrapper > div.text