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

ip = None
device = None

def some_function():
    from doiip.doiip import ask_select_account_doiip
    # sử dụng ask_select_account_doiip

# doiip.py
def some_other_function(message):
    from main import start

    start(message)
    # sử dụng start
############################ CHỨC NĂNG CHÍNH ##########################
def ask_select_account_doiip(message):

    # IN RA MÀN HÌNH
    print(f"\n============= | YÊU CẦU NGƯỜI DÙNG CHỌN TÀI KHOẢN CẦN ĐỔI IP | =============")

    # YÊU CẦU NGƯỜI DÙNH CHỌN TÀI KHOẢN
    dylib.print_red("Đang đợi người dùng chọn tài khoản cần đổi IP...")
    

    markup = types.ReplyKeyboardMarkup(row_width=3)
    button_nickphulbh = types.KeyboardButton('Nick Phụ LBH')
    button_nickchinhvanbao = types.KeyboardButton('Nick Chính Văn Bảo')
    button_memelo = types.KeyboardButton('Nick MEME LỎ')
    home = types.KeyboardButton('Trở lại menu chính')
    markup.add(button_nickphulbh, button_nickchinhvanbao, button_memelo, home)

    # GỬI TIN NHẮN CHO NGƯỜI DÙNG
    bot.send_message(message.chat.id, "Vui lòng chọn tài khoản cần đổi IP", reply_markup=markup)

    bot.register_next_step_handler(message, doiip)

def doiip(message):
    global ip
    global device

    if message.text == "Nick Phụ LBH":
        dylib.bot_reply(user_id, "Tiến hành đổi IP & thiết bị cho tài khoản Nick Phụ LBH") ; dylib.print_green("Tiến hành đổi IP & thiết bị cho tài khoản Nick Phụ LBH")
        ip = "ip-22680"
        device = "renew-22680"
    elif message.text == "Nick Chính Văn Bảo":
        dylib.bot_reply(user_id, "Tiến hành đổi IP & thiết bị cho tài khoản Nick Chính Văn Bảo") ; dylib.print_green("Tiến hành đổi IP & thiết bị cho tài khoản Nick Chính Văn Bảo")
        ip = "ip-22679"
        device = "renew-22679"
    elif message.text == "Nick MEME LỎ":
        dylib.bot_reply(user_id, "Tiến hành đổi IP & thiết bị cho tài khoản Nick Meme Lỏ") ; dylib.print_green("Tiến hành đổi IP & thiết bị cho tài khoản Nick Meme Lỏ")
        ip = "ip-22733"
        device = "renew-22733"
    elif message.text == "Trở lại menu chính":
        some_other_function(message)
    else:
        return

    dylib.bot_reply(user_id, "Tiến hành mở website livestream") ; dylib.print_red("Mở website livestream")

    # KHỞI TẠO WEB DRIVER
    driver = webdriver.Chrome(service=service, options=options) ; dylib.print_green("Khởi tạo chrome web driver")

    # MỞ WEB LIVESTREAM
    driver.get('https://autolive.me/tiktok')

    # KIỂM TRA XEM TRANG WEB LOAD XONG CHƯA
    try:
        # IN RA MÀN HÌNH
        dylib.print_green_and_send_message(user_id, "Đang load trang web livestream...")

        # ĐỢI PHẦN TỬ CỦA WEB XUẤT HIỆN
        # SAU KHI PHẦN TỬ XUẤT HIỆN => GỬI TIN NHẮN CHO NGƯỜI DÙNG VÀ IN RA MÀN HÌNH ĐỂ THÔNG BÁO
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b'))) ; dylib.print_yellow_and_send_message(user_id, "Load website livestream thành công")
    except TimeoutError:
        # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG NẾU THẤT BẠI
        dylib.print_green_and_send_message(user_id, "Có lỗi xảy ra khi truy cập vào trang web livestream, vui lòng kiểm tra lại kết nối internet của máy chủ.")

        # ĐÓNG CHROME
        driver.quit()

        # KẾT THÚC TIẾN TRÌNH
        return

    # CLICK VÀO NÚT ĐỔI TK WEB
    dylib.print_green("Click vào nút đổi TK WEB"); driver.find_element(By.CSS_SELECTOR, "#formLive > div:nth-child(3) > div.col-md-3 > div > div > button:nth-child(2) > i").click()

    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dialog_tiktok > div > div > div")))

    # ĐỔI IP
    change_ip = f'document.getElementById("{ip}").click();'

    dylib.print_green("Click vào nút đổi IP"); driver.execute_script(change_ip) ; dylib.bot_reply(user_id, "Đang đổi IP...")

    # CHỜ ĐỢI THÔNG BÁO CỬ SỰ KIỆN ĐỔI IP XUẤT HIỆN
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))

    data_changeip = driver.execute_script('''
        // JavaScript code here
        // Đoạn mã JavaScript để lấy nội dung của phần tử
        var element = document.querySelector('div.text[data-notify-html="text"]');
        return element.textContent;
    ''')

    if data_changeip == "Thành công":

        # DỮ LIỆU CỦA THÔNG BÁO ĐỔI IP
        dylib.bot_reply(user_id, f"Đổi IP thành công") ; dylib.print_yellow(f"Thông báo của web sau khi đổi IP: {data_changeip}")

    else:
        dylib.print_yellow_and_send_message(user_id, f"Đổi IP thất bại\nThông báo của web:\n{data_changeip}")

        driver.quit()

    # MỞ WEB LIVESTREAM
    driver.get('https://autolive.me/tiktok')

    # KIỂM TRA XEM TRANG WEB LOAD XONG CHƯA
    try:
        # ĐỢI PHẦN TỬ CỦA WEB XUẤT HIỆN
        # SAU KHI PHẦN TỬ XUẤT HIỆN => GỬI TIN NHẮN CHO NGƯỜI DÙNG VÀ IN RA MÀN HÌNH ĐỂ THÔNG BÁO
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))
    except TimeoutError:

        # ĐÓNG CHROME
        driver.quit()

        # KẾT THÚC TIẾN TRÌNH
        return
    
    # CLICK VÀO NÚT ĐỔI TK WEB
    dylib.print_green("Click vào nút đổi TK WEB"); driver.find_element(By.CSS_SELECTOR, "#formLive > div:nth-child(3) > div.col-md-3 > div > div > button:nth-child(2) > i").click()

    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dialog_tiktok > div > div > div")))

    # ĐỔI THIẾT BỊ
    change_device = f'document.getElementById("{device}").click();'
    driver.execute_script(change_device) ; dylib.print_green("Click vào nút đổi THIẾT BỊ"); dylib.bot_reply(user_id, "Đang đổi THIẾT BỊ...")

    # CHỜ ĐỢI THÔNG BÁO CỬ SỰ KIỆN ĐỔI THIẾT BỊ XUẤT HIỆN
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))

    data_changdevice = driver.execute_script('''
        // JavaScript code here
        // Đoạn mã JavaScript để lấy nội dung của phần tử
        var element = document.querySelector('div.text[data-notify-html="text"]');
        return element.textContent;
    ''')

    if data_changdevice == "Thành công":
        # DỮ LIỆU CỦA THÔNG BÁO ĐỔI IP
        dylib.bot_reply(user_id, f"Đổi thiết bị thành công") ; dylib.print_yellow(f"Thông báo của web sau khi đổi thiết bị: {data_changdevice}")
        driver.quit()

    else:
        dylib.print_yellow_and_send_message(user_id, f"Đổi thiết bị thất bại\nThông báo của web: {data_changdevice}")
        driver.quit()