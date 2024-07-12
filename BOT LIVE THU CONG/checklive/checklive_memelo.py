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

# THÔNG TIN TÀI KHOẢN LIVE
ten_tai_khoan = "MEME LỎ"
id_tiktok = "meme.l810"
select_account = "#tiktok_account > option:nth-child(5)"

# LINK NGUỒN CHO PHIÊN LIVE 
from nguonlive.linknguon import linknguon

# Khởi tạo colorama
init()

############################ CHỨC NĂNG CHÍNH ##########################
def main_checklive_memelo(message):

    print(f"\n============= CHECK LIVE TÀI KHOẢN | {Fore.GREEN}{ten_tai_khoan}{Style.RESET_ALL} | ID Tiktok: {id_tiktok}=============")

     # KHỞI TẠO WEB DRIVER
    driver = webdriver.Chrome(service=service, options=options)

    # IN RA MÀN HÌNH
    dylib.print_yellow("KHỞI TẠO WEB DRIVER\n")

    # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
    dylib.print_red_and_send_message(user_id, f"Tiến hành kiểm tra phiên livestream tài khoản {ten_tai_khoan}")

    sleep(1) # CHỜ 1 GIÂY

    # IN RA MÀN HÌNH
    dylib.print_yellow("Truy cập phiên livestream")

    # KIỂM TRA XEM CÓ TRUY CẬP PHIÊN LIVE THÀNH CÔNG HAY KHÔNG
    try:
        # MỞ PHIÊN LIVE
        driver.get('https://www.tiktok.com/@vanbao165201/live')

        # ĐỢI PHIÊN LIVE LOAD HOÀN TẤT
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[1]/div/div[1]/a')))

        # IN RA MÀN HÌNH VÀ GỬI TIN NHẮN
        dylib.print_yellow_and_send_message(user_id, "Truy cập phiên livestream thành công, tiến hành kiểm tra\nKhi nào phiên live dưới 5 người xem tôi sẽ thông báo cho bạn")
    except TimeoutException:
        # IN RA MÀN HÌNH
        dylib.print_red_and_send_message(user_id, "Truy cập phiên livestream thất bại, vui lòng kiểm tra lại")

        # ĐÓNG CHROME
        driver.quit()

        # KẾT THÚC TIẾN TRÌNH
        return
    
    # KIỂM TRA SỐ LƯỢNG NGƯỜI XEM CỦA PHIÊN LIVE
    while True:
        # KIỂM TRA LẦN 1
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))
            now = datetime.datetime.now()
            
            checkview = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div")
            view = checkview.text

            if int(view) > 5:
                print(f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live hiện tại có {view} người xem => TIẾP TỤC KIỂM TRA...")
                driver.refresh()
            else:
                bot_reply_and_print(message, f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live hiện tại đang có {view} người xem => Tiến hành tắt live")
                driver.quit()
                tatlive(message)
                return
        except TimeoutException:
            bot_reply_and_print(message, "Không check được số người xem live, có vẻ như phiên live đã bị sập.")
            driver.quit()
            return    