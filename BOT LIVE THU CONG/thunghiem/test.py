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

user_id = '6355094590' # ID CỦA NGƯỜI DÙNG

# THÔNG TIN TÀI KHOẢN LIVE
ten_tai_khoan = "NICK PHU LBH"
id_tiktok = "nammapsang_keorank"

# LINK NGUỒN CHO PHIÊN LIVE 
from nguonlive.linknguon import linknguon

############################ CHỨC NĂNG CHÍNH ##########################
def main_test(message):

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
        driver.get(f'https://www.tiktok.com/@{id_tiktok}/live')

        # ĐỢI PHIÊN LIVE LOAD HOÀN TẤT
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div[1]/a')))

        # IN RA MÀN HÌNH VÀ GỬI TIN NHẮN
        dylib.print_yellow_and_send_message(user_id, "Khi nào phiên live được diễn ra tôi sẽ thông báo cho bạn")
    except TimeoutException:
        # IN RA MÀN HÌNH
        dylib.print_red_and_send_message(user_id, "Sảy ra sự cố khi truy cập phiên live, vui lòng kiểm tra lại kết nối internet")

        # ĐÓNG CHROME
        driver.quit()

        # KẾT THÚC TIẾN TRÌNH
        return
    
    while True:
        now = datetime.datetime.now()
        try:
            # KIỂM TRA PHẦN TỬ CHỨA SỐ LƯỢNG NGƯỜI XEM

            # SỬ DỤNG WebDriverWait, NẾU TRONG 1 GIÂY MÀ PHẦN TỬ XUẤT HIỆN THÌ PHIÊN LIVE ĐÃ ĐƯỢC MỞ
            checkview = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#tiktok-live-main-container-id > div.css-1fxlgrb-DivBodyContainer.etwpsg30 > div.css-l1npsx-DivLiveContentContainer.etwpsg31 > div > div.css-wl3qaw-DivLiveContent.e1nhv3vq1 > div.css-1kgwg7s-DivLiveRoomPlayContainer.e1nhv3vq2 > div.css-jvdmd-DivLiveRoomBanner.e10bhxlw0 > div.css-1s7wqxh-DivUserHoverProfileContainer.e19m376d0 > div > div > div.css-1j46cc2-DivExtraContainer.e1571njr9 > div.css-9aznci-DivLivePeopleContainer.e1571njr10 > div > div"))
            )
            dylib.print_red_and_send_message(user_id, f"Phiên live đã được diễn ra vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")
            
            # ĐÓNG TRÌNH DUYỆT CHROME
            driver.quit()

            # KẾT THÚC TIẾN TRÌNH
            return
        except TimeoutException:
            # IN RA MÀN HÌNH
            dylib.print_green(f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live chưa dược diễn ra => TIẾP TỤC KIỂM TRA")

            # LÀM MỚI LẠI PHIÊN LIVE
            driver.refresh()

            # KIỂM TRA XEM PHIÊN LIVE CÓ ĐƯỢC LÀM MỚI THÀNH CÔNG HAY KHÔNG SAU KHI LÀM MỚI
            try:
                WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[3]/div/div[1]/a"))
                )
            except TimeoutException:
                dylib.print_red_and_send_message(user_id, "Có lỗi sảy ra khi kiểm tra phiên live, vui lòng kiểm tra lại kết nối internet")