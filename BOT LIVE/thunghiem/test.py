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
    from dylib.dylib import close_existing_browser
    log_info("Đang chạy hàm kiểm tra các phiên trình duyệt đang chạy, nếu có phiên trình duyệt nào đang được sẽ đóng trình duyệt")
    close_existing_browser() # Đóng tất cả các phiên trình duyệt đang chạy
    # Khởi tạo chrome driver
    driver = webdriver.Chrome(service=service, options=options)

    driver.get('https://www.tiktok.com/@nammapsang_keorank/live')

    try:
        log_info("Đang load phiên live")
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div[1]/a')))

        bot_reply(user_id, "Truy cập phiên live thành công, khi nào phiên live diễn ra tôi sẽ thông báo cho bạn")
    except TimeoutException:
        bot_reply(user_id, "Không thể truy cập phiên live, xảy ra sự cố kết nối internet")
        log_info("Không thể truy cập phiên live do kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return
    
    # HÀM KIỂM TRA PHIÊN LIVE
    while True:
        now = datetime.datetime.now() # Biến lấy ngày giờ hiện tại của hệ thống
        try:
            log_info("Đang check view...")
            checkview = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))
            
            bot_reply(user_id, f"Check live hoàn tất, phiên live đã được mở vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")
            log_info(f"Phiên live đã được diễn ra vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")

            log_info("Đóng trình duyệt chrome")
            driver.quit()

            log_info("Kết thúc tiến trình")
            return
        except TimeoutException:
            log_info("Phiên live chưa được diễn ra")

            log_info("Làm mới lại phiên live")
            driver.refresh()

            # Kiểm tra xem có làm mới lại phiên live thành công hay không
            try:
                WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[3]/div/div[1]/a"))
                )
            except TimeoutException:
                bot_reply(user_id, "Kiểm tra phiên live thất bại do có sự cố kết nối internet, vui lòng kiểm tra lại đường truyền")
                log_error("Kiểm tra phiên live thất bại do có sự cố về kết nối internet")

                log_info("Đóng trình duyệt chrome")
                driver.quit()

                log_info("Kết thúc tiến trình")
                return