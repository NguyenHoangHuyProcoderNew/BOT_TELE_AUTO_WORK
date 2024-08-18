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
from telebot import types

# Đường dẫn đến chrome driver
chromedriver_path = r'D:\\BOT_TELE_AUTO_WORK\\BOT LIVE THU CONG\\chrome_driver\\chromedriver.exe'

# Cấu hình chrome driver
options = Options()
options.add_argument('--log-level=3')  # Vô hiệu hóa thông báo của Selenium
options.add_argument('--user-data-dir=D:\\BOT_TELE_AUTO_WORK\\BOT LIVE THU CONG\\du lieu trinh duyet')

service = Service(chromedriver_path)
service_log_path = os.path.devnull
service = Service(chromedriver_path, service_log_path=service_log_path)

# KHAI BÁO APT TOKEN BOT TELEGRAM
API_TOKEN = '7329003333:AAF7GhjivbGnk0jSGE8XfefFh_-shHAFsGc'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

# CÁC CHỨC NĂNG IN RA MÀN HÌNH
from print_logger.print_logger import log_info, log_warning, log_error, log_success

# Nhập chức năng bot phản hồi lại người dùng
from dylib.dylib import bot_reply

from dylib.dylib import user_id
from dylib.dylib import username

# Đường dẫn đến chrome driver
chromedriver_path = r'D:\\BOT_TELE_AUTO_WORK\\BOT LIVE THU CONG\\chrome_driver\\chromedriver.exe'

# Cấu hình chrome driver
options = Options()
options.add_argument('--log-level=3')  # Vô hiệu hóa thông báo của Selenium
options.add_argument('--user-data-dir=D:\\BOT_TELE_AUTO_WORK\\BOT LIVE THU CONG\\du lieu trinh duyet')

service = Service(chromedriver_path)
service_log_path = os.path.devnull
service = Service(chromedriver_path, service_log_path=service_log_path)


def main_test(message):
    # from dylib.dylib import close_existing_browser
    # log_info("Đang chạy hàm kiểm tra các phiên trình duyệt đang chạy, nếu có phiên trình duyệt nào đang được sẽ đóng trình duyệt")
    # close_existing_browser() # Đóng tất cả các phiên trình duyệt đang chạy
    # Khởi tạo chrome driver
    driver = webdriver.Chrome(service=service, options=options)

    # Mở trang web livestream
    bot_reply(user_id, "Đang mở trang web livestream")
    log_info("Mở trang web livestream")
    driver.get('https://autolive.me/tiktok')

    # Kiểm tra xem có load trang web livestream thành công hay không
    try:
        bot_reply(user_id, "Đang load trang web livestream...")
        log_info("Đang load trang web livestream")

        # Kiểm tra xem trang web đã load xong chưa
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))

        bot_reply(user_id, "Load trang web livestream thành công")
        log_success("Load trang web livestream thành công")
    except TimeoutError:
        bot_reply(user_id, "Load trang web livestream thất bại\nNguyên nhân: đường truyền internet quá yếu hoặc trang web sử dụng băng thông nước ngoài dẫn đến lỗi, kiểm tra lại kết nối internet của máy chủ")
        log_error("Load trang web livestream thất bại")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return

    # Chờ nút mở live xuất hiện lần 1
    log_info("Đang đợi nút mở phiên live xuất hiện")
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-status='1'][data-toggle='tooltip'][data-placement='top'][data-original-title='Bắt đầu live']"))
        )

        log_success("Nút mở live đã xuất hiện")
    except TimeoutException:
        log_error("Không tồn tại nút mở live")

        log_info("Làm mới lại trang web livestream")
        driver.refresh()

    # Chờ nút mở live xuất hiện lần 2
    log_info("Kiểm tra sự xuất hiện của nút mở live lần 2")
    
    log_info("Đang đợi nút mở phiên live xuất hiện")
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-status='1'][data-toggle='tooltip'][data-placement='top'][data-original-title='Bắt đầu live']"))
        )

        log_success("Nút mở live đã xuất hiện")
    except TimeoutException:
        log_error("Không tồn tại nút mở live")

        log_info("Làm mới lại trang web livestream")