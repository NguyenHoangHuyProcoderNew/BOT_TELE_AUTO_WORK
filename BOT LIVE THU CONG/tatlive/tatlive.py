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

green_text = "TẮT LIVE TÀI KHOẢN"

# Khởi tạo colorama
init()

########## TRỞ VỀ MENU CHÍNH #########
home = telebot.types.ReplyKeyboardMarkup(True).add("Đổi IP").add("Mở live").add("Tắt live")
def back_home(message):
    text = "VUI LÒNG CHỌN 👇"
    bot.send_message(message.chat.id, text, reply_markup=home)

# HÀM YÊU CẦU NGƯỜI DÙNG XÁC NHẬN TẮT PHIÊN LIVE (HỎI XEM NGƯỜI DÙNG CÓ MUỐN TẮT PHIÊN LIVE HIỆN TẠI KHÔNG?)
def xacnhan_tatlive(message):
    print("\n============= | NGƯỜI DÙNG YÊU CẦU TẮT PHIÊN LIVE HIỆN TẠI | =============")
    dylib.print_red("Đang đợi người dùng xác nhận...")

    # Tạo bàn phím xác nhận
    xacnhantatlive = telebot.types.ReplyKeyboardMarkup(True)
    xacnhantatlive.add('Có', 'Không').add('Trở lại menu chính')

    # Gửi tin nhắn yêu cầu xác nhận
    bot.send_message(message.chat.id, "Xác nhận tắt phiên live hiện tại?", reply_markup=xacnhantatlive)

    # Đăng ký xử lý bước tiếp theo
    bot.register_next_step_handler(message, main_tatlive)

# HÀM THỰC HIỆN VIỆC TẮT LIVE
def main_tatlive(message):
    if message.text == "Có":
        dylib.print_green_and_send_message(user_id, "Tiến hành mở trang web livestream")

        # KHỞI TẠO WEB DRIVER
        driver = webdriver.Chrome(service=service, options=options)
        dylib.print_green("KHỞI TẠO WEB DRIVER")

        # MỞ WEB LIVESTREAM
        dylib.print_green("Mở website livestream")
        driver.get('https://autolive.me/tiktok')

        # KIỂM TRA XEM TRANG WEB LOAD XONG CHƯA
        try:
            dylib.print_green("Đang load website...")
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b'))
            )
            dylib.print_yellow_and_send_message(user_id, "Mở website livestream thành công")
        except TimeoutError:
            dylib.print_yellow_and_send_message(user_id, "Mở website livestream thất bại")
            driver.quit()
            return

        dylib.print_red_and_send_message(user_id, "Tiến hành tắt live...")

        # KIỂM TRA SỰ KIỆN TẮT LIVE
        try:
            button_tatlive = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-original-title='Dừng live']"))
            )
            if button_tatlive.get_attribute("data-original-title") == "Dừng live":
                dylib.print_green("Click vào nút tắt live")
                button_tatlive.click()
        except:
            dylib.print_red_and_send_message(user_id, "Hiện tại không có phiên live nào được mở")
            driver.quit()
            return

        # KIỂM TRA SỰ KIỆN TẮT LIVE CÓ THÀNH CÔNG HAY KHÔNG
        try:
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div > div.notifyjs-container > div'))
            )
            dylib.print_yellow_and_send_message(user_id, "Tắt live thành công...!")
        except TimeoutException:
            dylib.print_red_and_send_message(user_id, "Tắt live không thành công")
        finally:
            driver.quit()
            return
    elif message.text in ["Không", "Trở lại menu chính"]:
        back_home(message)
