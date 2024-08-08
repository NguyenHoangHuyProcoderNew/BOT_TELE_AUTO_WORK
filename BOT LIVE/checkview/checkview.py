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
API_TOKEN = '7371036517:AAEB8PtQRtSrvDOxQUUW2su7ObGso6ltq8w'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

user_id = '5634845912' # ID CỦA NGƯỜI DÙNG

id_tiktok = None

############################ CHỨC NĂNG CHÍNH ##########################

home = telebot.types.ReplyKeyboardMarkup(True).add("Đổi IP").add("Mở live").add("Tắt live").add("Check view")
def back_home(message):
    text = "VUI LÒNG CHỌN 👇"
    bot.send_message(message.chat.id, text, reply_markup=home)
    
def ask_select_account_checkview(message):
    print(f"============= | CHECK VIEW | =============")
    # HỎI NGƯỜI DÙNG MUỐN VIEW TÀI KHOẢN NÀO?
    dylib.print_red("Bot đang đợi người dùng chọn tài khoản cần check view...")
    button_select_account_checkview = telebot.types.ReplyKeyboardMarkup(True).add("Nick Văn Bảo").add("Nick Phụ LBH").add("Nick MEME Lỏ").add("Trở lại menu chính")
    text = "Vui lòng chọn tài khoản cần check view"
    bot.send_message(message.chat.id, text, reply_markup=button_select_account_checkview)

    bot.register_next_step_handler(message, checkview_main)

def checkview_main(message):
    global id_tiktok

    if message.text == "Nick Văn Bảo":
        id_tiktok = "vanbao165201"
        dylib.print_red_and_send_message(user_id, "Tiến hành check view cho tài khoản Văn Bảo")
    elif message.text == "Nick Phụ LBH":
        id_tiktok = "nammapsang_keorank"
        dylib.print_red_and_send_message(user_id, "Tiến hành check view cho tài khoản Nick Phụ LBH")
    elif message.text == "Nick MEME Lỏ":
        id_tiktok = "meme.l810"
        dylib.print_red_and_send_message(user_id, "Tiến hành check view cho tài khoản MEME Lỏ")

    # KHỞI TẠO WEB DRIVER
    driver = webdriver.Chrome(service=service, options=options)
    dylib.print_green("KHỞI TẠO WEB DRIVER")

    # MỞ PHIÊN LIVE
    dylib.print_green_and_send_message(user_id, "Đang mở phiên live...")
    driver.get(f'https://www.tiktok.com/@{id_tiktok}/live')

    # BIẾN LẤY THỜI GIAN HIỆN TẠI
    now = datetime.datetime.now()

    # KIỂM TRA XEM PHIÊN LIVE CÓ LOAD THÀNH CÔNG HAY KHÔNG
    try:
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[3]/div/div[1]/a"))
        )
    except TimeoutException:
        # IN RA MÀN HÌNH VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
        dylib.print_yellow_and_send_message(user_id, "Có lỗi sảy ra khi kiểm tra phiên live, vui lòng kiểm tra lại kết nối internet")

        # ĐÓNG CHROME
        driver.quit()

        return # KẾT THÚC TIẾN TRÌNH
    
    # ĐỢI PHẦN TỬ CHỨA SỐ LƯỢNG NGƯỜI XEM LIVE XUẤT HIỆN
    checkview = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#tiktok-live-main-container-id > div.css-1fxlgrb-DivBodyContainer.etwpsg30 > div.css-l1npsx-DivLiveContentContainer.etwpsg31 > div > div.css-wl3qaw-DivLiveContent.e1nhv3vq1 > div.css-1kgwg7s-DivLiveRoomPlayContainer.e1nhv3vq2 > div.css-jvdmd-DivLiveRoomBanner.e10bhxlw0 > div.css-1s7wqxh-DivUserHoverProfileContainer.e19m376d0 > div > div > div.css-1j46cc2-DivExtraContainer.e1571njr9 > div.css-9aznci-DivLivePeopleContainer.e1571njr10 > div > div"))
    )

    # CHUYỂN SỐ LƯỢNG NGƯỜI XEM THÀNH VĂN BẢN
    view = checkview.text

    if int(view) >= 0:
        # GỬI SỐ LƯỢNG NGƯỜI XEM CHO NGƯỜI DÙNG
        dylib.print_green("Gửi số lượng người xem cho người dùng")
        dylib.bot_reply(user_id, f"{now.strftime('%d/%m/%Y %H:%M:%S')} Phiên live đã live được , hiện tại đang có {view} người xem")

        # ĐÓNG TRÌNH DUYỆT
        driver.quit()
    else:
        dylib.bot_reply(user_id, "Phiên live này hiện tại không được mở")