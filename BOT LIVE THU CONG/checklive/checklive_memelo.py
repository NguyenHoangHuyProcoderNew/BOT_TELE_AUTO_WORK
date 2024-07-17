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
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-images")
options.add_argument("--disable-javascript")

service = Service(chromedriver_path)
service_log_path = os.path.devnull
service = Service(chromedriver_path, service_log_path=service_log_path)

# KHAI BÁO APT TOKEN BOT TELEGRAM
API_TOKEN = '7329003333:AAF7GhjivbGnk0jSGE8XfefFh_-shHAFsGc'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

user_id = '6355094590' # ID CỦA NGƯỜI DÙNG

# THÔNG TIN TÀI KHOẢN LIVE
ten_tai_khoan = "MEME LỎ"
id_tiktok = "meme.l810"

# LINK NGUỒN CHO PHIÊN LIVE 
from nguonlive.linknguon import linknguon

# Khởi tạo colorama
init()

############################ CHỨC NĂNG CHÍNH ##########################
def main_checklive_memelo(message):

    print(f"\n============= KIỂM TRA PHIÊN LIVE CỦA TÀI KHOẢN | {Fore.GREEN}{ten_tai_khoan}{Style.RESET_ALL} | ID Tiktok: {id_tiktok} =============")

    # Gửi tin nhắn cho người dùng
    dylib.bot_reply(user_id, f"Tiến hành thực thi lệnh kiểm tra phiên live cho tài khoản {ten_tai_khoan} có ID tiktok: {id_tiktok}")

    # Gửi tin nhắn cho người dùng
    dylib.bot_reply(user_id, "Truy cập vào phiên live")

     # KHỞI TẠO WEB DRIVER
    driver = webdriver.Chrome(service=service, options=options)

    # IN RA MÀN HÌNH
    dylib.print_red("KHỞI TẠO WEB DRIVER\n")

    # MỞ PHIÊN LIVE
    dylib.print_green(f"Mở phiên livestream với URL: https://www.tiktok.com/@{id_tiktok}/live") ; driver.get(f'https://www.tiktok.com/@{id_tiktok}/live')

    # KIỂM TRA XEM CÓ TRUY CẬP PHIÊN LIVE THÀNH CÔNG HAY KHÔNG
    try:
        # ĐỢI LOAD WEBSITE
        dylib.print_green_and_send_message(user_id, "Phiên live đang được load, vui lòng chờ...")

        # ĐỢI PHẦN TỬ CỦA WEBSITE XUẤT HIỆN, SAU KHI PHẦN TỬ XUẤT HIỆN THÌ => LOAD HOÀN TẤT
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div[1]/a'))) ; dylib.print_green("Load trang web thành công => TIẾN HÀNH KIỂM TRA") ; dylib.bot_reply(user_id, "Trang web đã load xong") ; sleep(1) ; dylib.bot_reply(user_id, "Khi nào phiên live dưới 5 người xem tôi sẽ tự động tắt live")

    except TimeoutException:
        dylib.print_yellow("Load website thất bại => KẾT THÚC TIẾN TRÌNH") ; dylib.bot_reply(user_id, "Trang web load không thành công, vui lòng kiểm tra lại kết nối internet của thiết bị")

        # ĐÓNG CHROME
        driver.quit()

        # KẾT THÚC TIẾN TRÌNH
        return
    
    # KIỂM TRA PHIÊN LIVE
    while True:
        now = datetime.datetime.now() # HÀM LẤY NGÀY GIỜ HIỆN TẠI CỦA THIẾT BỊ

        # IN RA MÀN HÌNH
        dylib.print_green(f"Đang check dữ liệu của phiên live vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}...")

        try:
            # CHECK DỮ LIỆU CỦA BIẾN CHỨA SỐ LƯỢNG NGƯỜI XEM
            checkview = WebDriverWait(driver, 1000).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#tiktok-live-main-container-id > div.css-1fxlgrb-DivBodyContainer.etwpsg30 > div.css-l1npsx-DivLiveContentContainer.etwpsg31 > div > div.css-wl3qaw-DivLiveContent.e1nhv3vq1 > div.css-1kgwg7s-DivLiveRoomPlayContainer.e1nhv3vq2 > div.css-jvdmd-DivLiveRoomBanner.e10bhxlw0 > div.css-1s7wqxh-DivUserHoverProfileContainer.e19m376d0 > div > div > div.css-1j46cc2-DivExtraContainer.e1571njr9 > div.css-9aznci-DivLivePeopleContainer.e1571njr10 > div > div"))
            )

            # CHUYỂN DỮ LIỆU CỦA PHẦN TỬ CHỨA SỐ LƯỢNG NGƯỜI XEM THÀNH VĂN BẢN
            view = checkview.text

            # ĐIỀU KIỆN KIỂM TRA NHƯ SAU:
            # NẾU DỮ LIỆU CỦA BIẾN view TRÊN 5 THÌ SẼ ĐÓNG CHROME TRƯỚC, RỒI MỞ LẠI, SAU ĐÓ TRUY CẬP PHIÊN LIVE VÀ TIẾP TỤC KIỂM TRA
            if int(view) > 5:
                # GỬI TIN NHẮN VỀ CHO NGƯỜI DÙNG
                dylib.print_green(f"Phiên live vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')} có {view} người xem => TIẾP TỤC KIỂM TRA")

                # IN RA MÀN HÌNH
                dylib.print_green("Đóng trình duyệt")

                # ĐÓNG CHROME
                driver.quit()

                # IN RA MÀN HÌNH
                dylib.print_green("Khởi tạo lại driver mới")
                
                # KHỞI TẠO LẠI DRIVER MỚI
                driver = webdriver.Chrome(service=service, options=options)

                # KIỂM TRA XEM CÓ TRUY CẬP PHIÊN LIVE THÀNH CÔNG HAY KHÔNG
                try:
                    # IN RA MÀN HÌNH
                    dylib.print_green("Truy cập vào phiên live")

                    # MỞ PHIÊN LIVE
                    driver.get(f'https://www.tiktok.com/@{id_tiktok}/live')

                    # ĐỢI PHIÊN LIVE LOAD HOÀN TẤT
                    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div[1]/a')))

                    # IN RA MÀN HÌNH VÀ GỬI TIN NHẮN
                    dylib.print_green("Truy cập phiên live thành công => tiến hành kiểm tra")
                except TimeoutException:
                    # IN RA MÀN HÌNH
                    dylib.print_green_and_send_message(user_id, "Truy cập phiên livestream thất bại, vui lòng kiểm tra lại")

                    # ĐÓNG CHROME
                    driver.quit()

                    # KẾT THÚC TIẾN TRÌNH
                    return    
            else:
                # GỬI TIN NHẮN CHO NGƯỜI DÙNG VÀ IN RA MÀN HÌNH
                dylib.print_yellow_and_send_message(user_id, f"Phiên live vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')} có {view} người xem => TIẾN HÀNH TẮT LIVE")
            
        except TimeoutException:
            # IN RA MÀN HÌNH
            dylib.print_yellow_and_send_message(user_id, "Có lỗi sảy ra khi kiểm tra phiên live, vui lòng kiểm tra lại kết nối internet")
            
            # ĐÓNG CHROME
            driver.quit()

            # KẾT THÚC TIẾN TRÌNH
            return