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
ten_tai_khoan = "MEME LỎ"
id_tiktok = "vanbao165201"
select_account = "#tiktok_account > option:nth-child(5)"

# LINK NGUỒN CHO PHIÊN LIVE 
from nguonlive.linknguon import linknguon

# Khởi tạo colorama
init()

############################ CHỨC NĂNG CHÍNH ##########################
def main_test(message):

    

     # KHỞI TẠO WEB DRIVER
    driver = webdriver.Chrome(service=service, options=options)

    # IN RA MÀN HÌNH
    dylib.print_yellow("Truy cập phiên livestream")
   

    # KIỂM TRA XEM PHIÊN LIVE ĐƯỢC MỞ HAY CHƯA
    try:
        # MỞ PHIÊN LIVE
        driver.get(f'https://www.tiktok.com/@{id_tiktok}/live') 

        # ĐỢI PHIÊN LIVE LOAD XONG
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tiktok-live-main-container-id > div.css-iozudi-DivHeaderContainer.e10win0d0 > div > div.css-oteyea-DivLeftContainer.e7nz4yf0 > a > svg')))

        # IN RA MÀN HÌNH
        dylib.print_red("Truy cập phiên livestream thành công")

        # IN RA MÀN HÌNH VÀ GỬI TIN NHẮN
        dylib.print_green_and_send_message(user_id, "Tiến hành kiểm tra thời điểm phiên live được mở")
        
        # KIỂM TRA SỐ LƯỢNG NGƯỜI XEM ĐỂ XÁC ĐỊNH PHIÊN LIVE ĐƯỢC MỞ HAY CHƯA
        while True:
            # CHỜ WEB LOAD XONG SAU KHI REFESH LẠI TRANG
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tiktok-live-main-container-id > div.css-iozudi-DivHeaderContainer.e10win0d0 > div > div.css-oteyea-DivLeftContainer.e7nz4yf0 > a > svg')))

            # CHỜ PHẦN TỬ CHỨA SỐ LƯỢNG NGƯỜI XEM XUẤT HIỆN
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))

            now = datetime.datetime.now()

            try:
                # LẤY DỮ LIỆU CỦA PHẦN TỬ CHỨA SỐ LƯỢNG NGƯỜI XEM CHUYỂN THÀNH VĂN BẢN 
                # VÀ KIỂM TRA DỮ LIỆU BẰNG ĐIỀU KIỆN IF
                element = driver.find_element(By.CSS_SELECTOR, "#tiktok-live-main-container-id > div.css-1fxlgrb-DivBodyContainer.etwpsg30 > div.css-l1npsx-DivLiveContentContainer.etwpsg31 > div > div.css-wl3qaw-DivLiveContent.e1nhv3vq1 > div.css-1kgwg7s-DivLiveRoomPlayContainer.e1nhv3vq2 > div.css-jvdmd-DivLiveRoomBanner.e10bhxlw0 > div.css-1s7wqxh-DivUserHoverProfileContainer.e19m376d0 > div > div > div.css-1j46cc2-DivExtraContainer.e1571njr9 > div.css-9aznci-DivLivePeopleContainer.e1571njr10 > div > div")
                view = element.text

                # NẾU SỐ LƯỢNG NGƯỜI XEM TỪ 0 TRỞ LÊN => PHIÊN LIVE ĐÃ ĐƯỢC MỞ
                if int(view) >= 0:
                    dylib.print_yellow_and_send_message(user_id, f"Phiên live đã được diễn ra vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")
                    driver.quit()
                    break
            # NẾU CHƯA ĐƯỢC DIỄN RA THÌ TIẾP TỤC KIỂM TRA            
            except NoSuchElementException:
                # IN RA MÀN HÌNH
                dylib.print_green(f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live chưa được diễn ra => Tiếp tục kiểm tra")
                driver.refresh()
    except TimeoutError:
        # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
        dylib.print_red_and_send_message(user_id, "Kiểm tra thất bại")

        # ĐÓNG CHROME
        driver.quit()

        # KẾT THÚC TIẾN TRÌNH
        return