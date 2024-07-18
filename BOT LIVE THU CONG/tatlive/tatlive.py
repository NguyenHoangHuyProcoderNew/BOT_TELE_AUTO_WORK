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

green_text = "TẮT LIVE TÀI KHOẢN"

# Khởi tạo colorama
init()

############################ CHỨC NĂNG CHÍNH ##########################
def main_tatlive(message):
    # IN RA MÀN HÌNH
    print(f"\n============= | {Fore.GREEN}{green_text}{Style.RESET_ALL} | =============")

    # GỬI TIN NHẮN CHO NGƯỜI DÙNG
    dylib.bot_reply(user_id, "THỰC THI LỆNH THÀNH CÔNG")

    # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
    dylib.print_green_and_send_message(user_id, "Tiến hành mở trang web livestream")    

     # KHỞI TẠO WEB DRIVER
    driver = webdriver.Chrome(service=service, options=options)

    # IN RA MÀN HÌNH
    dylib.print_red("KHỞI TẠO WEB DRIVER\n")

    # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
    dylib.print_green("Mở website livestream")

    # MỞ WEB LIVESTREAM
    driver.get('https://autolive.me/tiktok')

    # KIỂM TRA XEM TRANG WEB LOAD XONG CHƯA
    try:
        # IN RA MÀN HÌNH
        dylib.print_green("Đang load website...")

        # ĐỢI PHẦN TỬ CỦA WEB XUẤT HIỆN
        # SAU KHI PHẦN TỬ XUẤT HIỆN => KẾT LUẬN WEB ĐÃ LOAD XONG
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))

        # IN VÀ GỬI TIN NHẮN
        dylib.print_yellow_and_send_message(user_id, "Mở website livestream thành công")
    except TimeoutError:
        # IN VÀ GỬI TIN NHẮN
        dylib.print_yellow_and_send_message(user_id, "Mở website livestream thất bại")

        # ĐÓNG CHROME
        driver.quit()

        # KẾT THÚC TIẾN TRÌNH
        return

    #  IN RA MÀN HÌNH
    dylib.print_yellow_and_send_message(user_id, "Tiến hành tắt live...")

    # KIỂM TRA SỰ KIỆN TẮT LIVE
    try:
        # Kiểm tra giá trị data-original-title của button 
        # (Nếu là Dừng live thì mới click)
        button_tatlive = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-original-title='Dừng live']"))
    )
        if button_tatlive.get_attribute("data-original-title") == "Dừng live":
            
            # IN RA MÀN HÌNH
            dylib.print_green("Click vào nút tắt live")
            button_tatlive.click() # CLICK VÀO NÚT TẮT LIVE NẾU GIÁ TRỊ HỢP LỆ                                     
    except:
        dylib.print_red_and_send_message(user_id, "Hiện tại không có phiên live nào được mở")
        driver.quit()
        return

    # KIỂM TRA SỰ KIỆN TẮT LIVE CÓ THÀNH CÔNG HAY KHÔNG
    try:
        # CHỜ DỢI THÔNG BÁO TẮT LIVE XUẤT HIỆN
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div > div.notifyjs-container > div'))) # ĐỢI THÔNG BÁO TẮT LIVE THÀNH CÔNG XUẤT HIỆN

        # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
        dylib.print_yellow_and_send_message(user_id, "Tắt live thành công...!")

        # ĐÓNG CHROME
        driver.quit()

        # KẾT THÚC TIẾN TRÌNH
        return
    except TimeoutException:
        # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
        dylib.print_red_and_send_message(user_id, "Tắt live không thành công")

        # ĐÓNG CHROME
        driver.quit()

        # KẾT THÚC TIẾN TRÌNH
        return