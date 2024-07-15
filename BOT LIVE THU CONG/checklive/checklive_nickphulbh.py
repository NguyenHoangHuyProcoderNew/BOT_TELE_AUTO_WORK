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

# Khởi tạo colorama
init()

############################ CHỨC NĂNG CHÍNH ##########################
def main_checklive_nickphulbh(message):

    print(f"\n============= CHECK LIVE TÀI KHOẢN | {Fore.GREEN}{ten_tai_khoan}{Style.RESET_ALL} | ID Tiktok: {id_tiktok} =============")

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
        dylib.print_yellow_and_send_message(user_id, "Truy cập phiên live thành công, khi nào dưới 5 người xem sẽ tự động tắt live")
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
            # ĐỢI WEB LIVE LOAD XONG
            WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div[1]/a')))

            now = datetime.datetime.now()
            
            # ĐỢI PHẦN TỬ CHỨA SỐ LƯỢNG NGƯỜI XEM LIVE XUẤT HIỆN
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))

            # CHECK DỮ LIỆU CỦA PHẦN TỬ CHỨA SỐ LƯỢNG NGƯỜI XEM
            checkview = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div")

            # CHUYỂN DỮ LIỆU THÀNH VĂN BẢN
            view = checkview.text

            # NẾU PHIÊN LIVE TRÊN 5 NGƯỜI XEM THÌ TIẾP TỤC KIỂM TRA
            if int(view) > 5:
                dylib.print_green(f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live hiện tại có {view} người xem => TIẾP TỤC KIỂM TRA...")
                driver.refresh()
            else:
                # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
                dylib.print_yellow_and_send_message(message, f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live hiện tại đang có {view} người xem => Tiến hành tắt live")
                # ĐÓNG CHROME
                driver.quit()
                # KẾT THÚC TIẾN TRÌNH
                return
        except TimeoutException:
            # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
            dylib.print_red_and_send_message(user_id, "Kiểm tra phiên live lần 1 hoàn tất")
            # ĐÓNG CHROME
            driver.quit()

            # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
            dylib.print_yellow_and_send_message(user_id, "Tiến hành kiểm tra lần 2")

########################### KIỂM TRA LẦN 2 ############################

            # KHỞI TẠO WEB DRIVER
            driver = webdriver.Chrome(service=service, options=options)

            # IN RA MÀN HÌNH
            dylib.print_yellow("KHỞI TẠO WEB DRIVER\n")

            # IN RA MÀN HÌNH
            dylib.print_yellow("Truy cập phiên livestream")

            # KIỂM TRA XEM CÓ TRUY CẬP PHIÊN LIVE THÀNH CÔNG HAY KHÔNG
            try:
                # MỞ PHIÊN LIVE
                driver.get(f'https://www.tiktok.com/@{id_tiktok}/live')

                # ĐỢI PHIÊN LIVE LOAD HOÀN TẤT
                WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div[1]/a')))

                # IN RA MÀN HÌNH VÀ GỬI TIN NHẮN
                dylib.print_yellow_and_send_message(user_id, "Truy cập phiên live thành công, khi nào dưới 5 người xem sẽ tự động tắt live")
            except TimeoutException:
                # IN RA MÀN HÌNH
                dylib.print_red_and_send_message(user_id, "Truy cập phiên livestream thất bại, vui lòng kiểm tra lại")

                # ĐÓNG CHROME
                driver.quit()

                # KẾT THÚC TIẾN TRÌNH
                return
                        
            while True:
                # KIỂM TRA LẦN 2
                try:
                    # ĐỢI WEB LIVE LOAD XONG
                    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div[1]/a')))

                    now = datetime.datetime.now()
                    
                    # ĐỢI PHẦN TỬ CHỨA SỐ LƯỢNG NGƯỜI XEM LIVE XUẤT HIỆN
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))

                    # CHECK DỮ LIỆU CỦA PHẦN TỬ CHỨA SỐ LƯỢNG NGƯỜI XEM
                    checkview = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div")

                    # CHUYỂN DỮ LIỆU THÀNH VĂN BẢN
                    view = checkview.text

                    # NẾU PHIÊN LIVE TRÊN 5 NGƯỜI XEM THÌ TIẾP TỤC KIỂM TRA
                    if int(view) > 5:
                        dylib.print_green(f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live hiện tại có {view} người xem => TIẾP TỤC KIỂM TRA...")
                        driver.refresh()
                    else:
                        # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
                        dylib.print_yellow_and_send_message(message, f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live hiện tại đang có {view} người xem => Tiến hành tắt live")
                        # ĐÓNG CHROME
                        driver.quit()
                        # KẾT THÚC TIẾN TRÌNH
                        return
                # KẾT THÚC KIỂM TRA LẦN 2                    
                except TimeoutException:
                    # IN RA MÀN HÌNH
                    dylib.print_red_and_send_message(user_id, "Kiểm tra lần 2 hoàn tất")

                    # ĐÓNG CHROME
                    driver.quit()

                    # KẾT THÚC TIẾN TRÌNH
                    return                    