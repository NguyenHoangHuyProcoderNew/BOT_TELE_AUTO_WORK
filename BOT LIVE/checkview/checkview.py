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

id_tiktok = None

############################ CHỨC NĂNG CHÍNH ##########################

home = telebot.types.ReplyKeyboardMarkup(True).add("Đổi IP").add("Mở live").add("Tắt live").add("Check view")
def back_home(message):
    text = "VUI LÒNG CHỌN 👇"
    bot.send_message(message.chat.id, text, reply_markup=home)
    
def ask_select_account_checkview(message):
    log_info("Bot đang yêu cầu người dùng chọn tài khoản cần check view")
    button_select_account_checkview = telebot.types.ReplyKeyboardMarkup(True).add("Nick Văn Bảo").add("Nick Phụ LBH").add("Nick MEME Lỏ").add("Trở lại menu chính")
    bot.send_message(message.chat.id, "Vui lòng chọn tài khoản cần check view", reply_markup=button_select_account_checkview)

    bot.register_next_step_handler(message, checkview_main)

def checkview_main(message):
    global id_tiktok

    if message.text == "Nick Văn Bảo":
        id_tiktok = "vanbao165201"
        bot_reply(user_id, "Tiến hành check view cho Nick Văn Bảo")
        log_info("Người dùng đã chọn tài khoản Văn Bảo")
    elif message.text == "Nick Phụ LBH":
        id_tiktok = "nammapsang_keorank"
        bot_reply(user_id, "Tiến hành check view cho Nick Phụ LBH")
        log_info("Người dùng đã chọn Nick Phụ LBH")
    elif message.text == "Nick MEME Lỏ":
        id_tiktok = "meme.l810"
        bot_reply(user_id, "Tiến hành check view cho Nick Meme Lỏ")
    elif message.text == "Trở lại menu chính":
        log_info("Người dùng đã chọn Trở Lại Menu Chính")
        back_home(message)
        return

    log_info("Khởi tạo chrome driver")
    driver = webdriver.Chrome(service=service, options=options)
    
    bot_reply(user_id, "Tiến hành truy cập vào phiên live")
    log_info("Mở phiên livestream")
    driver.get(f'https://www.tiktok.com/@{id_tiktok}/live')

    try:
        log_info("Đang load phiên live...")

        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[3]/div/div[1]/a"))
        )

        bot_reply(user_id, "Truy cập phiên live thành công")
        log_info("Load phiên live thành công")
    except TimeoutException:
        bot_reply(user_id, "Truy cập phiên livestream thất bại\nNguyên nhân: đường truyền internet quá yếu hoặc trang web sử dụng băng thông nước ngoài dẫn đến lỗi, kiểm tra lại kết nối internet của máy chủ")
        log_error("Load trang web livestream thất bại")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return
    
    bot_reply(user_id, "Tiến hành check view...")
    log_info("Đang check view...")

    try:
        log_info("Đang đợi phần tử chứa số lượng người xem xuất hiện")
        # Đợi phần tử chứa số lượng người xem xuất hiện và kiểm tra dữ liệu của phần tử
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))

        log_info("Phần tử đã xuất hiện, tiến hành check view")

        checkview = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div")
        # Chuyển dữ liệu của phần tử chứa số lượng người xem thành văn bản
        view = checkview.text

        log_success("Check view thành công")
        if int(view) >= 0:
            log_info("Gửi dữ liệu cho người dùng")
            bot_reply(user_id, f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live hiện tại đang có {view} người xem")
    except TimeoutException:
        bot_reply(user_id, "Phiên live này hiện tại không được mở")
        log_error("Phần tử chứa số lượng người xem không xuất hiện, phiên live chưa được mở")
    finally:
        log_info("Đóng trình duyệt chrome")
        driver.quit()
        log_info("Kết thúc tiến trình")