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

# THÔNG TIN TÀI KHOẢN LIVE
ten_tai_khoan = "MEME LỎ"
id_tiktok = "meme.l810"
select_account = "#tiktok_account > option:nth-child(5)"

from colorama import Fore, Style, init

# Khởi tạo colorama
init()

############################ CHỨC NĂNG CHÍNH ##########################
def main_molive_memelo(message):

    print(f"\n============= MỞ LIVE TÀI KHOẢN | {Fore.GREEN}{ten_tai_khoan}{Style.RESET_ALL} | ID Tiktok: {id_tiktok}=============")

     # KHỞI TẠO WEB DRIVER
    driver = webdriver.Chrome(service=service, options=options)

    # IN RA MÀN HÌNH
    dylib.print_yellow("KHỞI TẠO WEB DRIVER\n")

    # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
    dylib.print_red_and_send_message(user_id, f"Tiến hành mở livestream tài khoản {ten_tai_khoan}")

    sleep(1) # CHỜ 1 GIÂY

    # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
    dylib.print_green("Mở website livestream")

    # MỞ WEB LIVESTREAM
    driver.get('https://autolive.me/tiktok')

    # KIỂM TRA XEM TRANG WEB LOAD XONG CHƯA
    try:
        # IN RA MÀN HÌNH
        dylib.print_green("Đang load website")

        # ĐỢI PHẦN TỬ CỦA WEB XUẤT HIỆN
        # SAU KHI PHẦN TỬ XUẤT HIỆN => KẾT LUẬN WEB ĐÃ LOAD XONG
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))

        # IN VÀ GỬI TIN NHẮN
        dylib.print_yellow_and_send_message(user_id, "Truy cập website livestream thành công")
    except TimeoutError:
        # IN VÀ GỬI TIN NHẮN
        dylib.print_red_and_send_message(user_id, "Truy cập website livestream thất bại")

        # ĐÓNG CHROME
        driver.quit()

        # KẾT THÚC TIẾN TRÌNH
        return

    # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
    dylib.print_yellow_and_send_message(user_id, "Tiến hành xóa cấu hình cũ")

    # XÓA CẤU HÌNH CŨ
    try:
        # IN RA MÀN HÌNH
        dylib.print_green("Click vào nút xóa cấu hình")

        # CLICK VÀO NÚT XÓA CẤU HÌNH
        driver.find_element(By.XPATH, '//button[@class="btn btn-circle btn-dark btn-sm waves-effect waves-light btn-status-live" and @data-status="-1" and @data-toggle="tooltip"]').click()

        # ĐỢI THÔNG BÁO XÓA CẤU HÌNH THÀNH CÔNG XUẤT HIỆN
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))

        # KIỂM TRA XEM CÓ CẤU HÌNH NÀO ĐANG CHẠY KHÔNG

        # LẤY DỮ LIỆU CỦA THÔNG BÁO XÓA CẤU HÌNH
        check_xoacauhinh = driver.find_element(By.CSS_SELECTOR, 'div.text[data-notify-html="text"]')

        # CHUYỂN DỮ LIỆU CHECK ĐƯỢC THÀNH VĂN BẢN
        data_xoacauhinh = check_xoacauhinh.text

        # KIỂM TRA DỮ LIỆU
        if data_xoacauhinh == "Bạn phải dừng luồng live trước khi xóa":
            dylib.print_red_and_send_message(user_id, "Không thể xóa cấu hình vì có 1 luồng live đang được chạy, vui lòng dừng live bằng lệnh /tatlive rồi thử lại sau")

            # ĐÓNG CHROME
            driver.quit()

            # DỪNG TIẾN TRÌNH
            return
    except:
        # IN RA MÀN HÌNH VÀ GỬI TIN NHẮN
        dylib.print_yellow_and_send_message(user_id, "Xóa cấu hình thành công")

    # CHỜ 1 GIÂY
    sleep(1)

    # IN VÀ GỬI TIN NHẮN
    dylib.print_yellow_and_send_message(user_id, "Tiến hành tạo cấu hình mới")

    # IN RA MÀN HÌNH
    dylib.print_green("Đang chọn tài khoản")
    driver.find_element(By.CSS_SELECTOR, f"{select_account}")