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

id_tiktok = None

############################ CHỨC NĂNG CHÍNH ##########################
def ask_select_account_checklive(message):
    # GỬI TIN NHẮN CHO NGƯỜI DÙNG
    dylib.bot_reply(user_id, "THỰC THI LỆNH THÀNH CÔNG")

    # IN RA MÀN HÌNH
    print(f"\n============= | YÊU CẦU NGƯỜI DÙNG CHỌN TÀI KHOẢN CẦN CHECK LIVE | =============")

    # YÊU CẦU NGƯỜI DÙNH CHỌN TÀI KHOẢN
    dylib.print_red("Đang đợi người dùng nhập ID TikTok của tài khoản cần checklive..."); dylib.bot_reply(user_id, "Vui lòng nhập ID TikTok của tài khoản cần checklive")

    bot.register_next_step_handler(message, checklive)

def checklive(message):
    global id_tiktok

    # NHẬN DỮ LIỆU MÀ NGƯỜI DÙNG NHẬP
    id_tiktok = message.text.strip()

    # THÔNG BÁO XÁC NHẬN NGƯỜI DÙNG ĐÃ NHẬP ID TIKTOK
    dylib.bot_reply(user_id, f"Tiến hành kiểm tra phiên livestream của tài khoản tiktok có ID {id_tiktok}") ; dylib.print_green(f"Người dùng đã nhập ID TikTok: {id_tiktok}")

    dylib.print_red_and_send_message(user_id, "Truy cập vào phiên live")

    # KHỞI TẠO WEB DRIVER
    driver = webdriver.Chrome(service=service, options=options) ; dylib.print_green("Khởi tạo chrome web driver")

    # MỞ PHIÊN LIVE
    driver.get(f'https://www.tiktok.com/@{id_tiktok}/live')

    # KIỂM TRA XEM TRANG WEB LOAD XONG CHƯA
    try:
        # IN RA MÀN HÌNH
        dylib.print_green_and_send_message(user_id, "Đang load phiên live...")

        # ĐỢI PHẦN TỬ CỦA WEB XUẤT HIỆN
        # SAU KHI PHẦN TỬ XUẤT HIỆN => GỬI TIN NHẮN CHO NGƯỜI DÙNG VÀ IN RA MÀN HÌNH ĐỂ THÔNG BÁO
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tiktok-live-main-container-id > div.css-iozudi-DivHeaderContainer.e10win0d0 > div > div.css-oteyea-DivLeftContainer.e7nz4yf0 > a'))) ; dylib.print_yellow_and_send_message(user_id, "Load phiên livestream thành công")
    except TimeoutError:
        # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG NẾU THẤT BẠI
        dylib.print_green_and_send_message(user_id, "Có lỗi xảy ra khi truy cập vào phiên livestream, vui lòng kiểm tra lại kết nối internet của máy chủ.")

        # ĐÓNG CHROME
        driver.quit()

        # KẾT THÚC TIẾN TRÌNH
        return

    # HÀM KIỂM TRA PHIÊN LIVE
    while True:
        now = datetime.datetime.now()
        try:
            # KIỂM TRA PHẦN TỬ CHỨA SỐ LƯỢNG NGƯỜI XEM

            # SỬ DỤNG WebDriverWait, NẾU TRONG 1 GIÂY MÀ PHẦN TỬ XUẤT HIỆN THÌ PHIÊN LIVE ĐÃ ĐƯỢC MỞ
            checkview = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#tiktok-live-main-container-id > div.css-1fxlgrb-DivBodyContainer.etwpsg30 > div.css-l1npsx-DivLiveContentContainer.etwpsg31 > div > div.css-wl3qaw-DivLiveContent.e1nhv3vq1 > div.css-1kgwg7s-DivLiveRoomPlayContainer.e1nhv3vq2 > div.css-jvdmd-DivLiveRoomBanner.e10bhxlw0 > div.css-1s7wqxh-DivUserHoverProfileContainer.e19m376d0 > div > div > div.css-1j46cc2-DivExtraContainer.e1571njr9 > div.css-9aznci-DivLivePeopleContainer.e1571njr10 > div > div"))
            )
            dylib.print_yellow_and_send_message(user_id, f"Phiên live đã được diễn ra vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")
            
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
                # IN RA MÀN HÌNH VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
                dylib.print_yellow_and_send_message(user_id, "Có lỗi sảy ra khi kiểm tra phiên live, vui lòng kiểm tra lại kết nối internet")

                # ĐÓNG CHROME
                driver.quit()

                return # KẾT THÚC TIẾN TRÌNH