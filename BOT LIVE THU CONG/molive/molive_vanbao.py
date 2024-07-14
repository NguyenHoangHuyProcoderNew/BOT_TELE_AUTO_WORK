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
ten_tai_khoan = "VĂN BẢO"
id_tiktok = "vanbao165201"
select_account = "#tiktok_account > option:nth-child(3)"

# LINK NGUỒN CHO PHIÊN LIVE 
from nguonlive.linknguon import linknguon

# Khởi tạo colorama
init()

############################ CHỨC NĂNG CHÍNH ##########################
def main_molive_vanbao(message):

    print(f"\n============= MỞ LIVE TÀI KHOẢN | {Fore.GREEN}{ten_tai_khoan}{Style.RESET_ALL} | ID Tiktok: {id_tiktok} =============")

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
    dylib.print_yellow_and_send_message(user_id, "Tạo cấu hình mới")

    # IN RA MÀN HÌNH
    dylib.print_green("Chọn tài khoản")

    # CHỌN TÀI KHOẢN LIVE
    driver.find_element(By.CSS_SELECTOR, f"{select_account}").click()

    # IN RA MÀN HÌNH
    dylib.print_green("Nhập tiêu đề live")

    # NHẬP TIÊU ĐỀ LIVE
    driver.find_element(By.ID, "title").send_keys('kéo rank Liên Quân')

    # IN RA MÀN HÌNH
    dylib.print_green("Chọn chủ đề live")

    # CHỌN CHỦ ĐỀ LIVE
    driver.find_element(By.CSS_SELECTOR, "#topic > option:nth-child(11)").click()

    # IN RA MÀN HÌNH
    dylib.print_green("Chọn kiểu live Mobile")

    # CHỌN KIỂU LIVE
    driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div/div[3]/div/div/div[2]/form/div[4]/div/div/div/button[2]").click()

    # IN RA MÀN HÌNH
    dylib.print_green("Nhập link nguồn cho phiên live")

    # NHẬP LINK NGUỒN
    driver.find_element(By.ID, "url_source").send_keys(linknguon)

    # IN RA MÀN HÌNH
    dylib.print_yellow("Lưu cấu hình")

    # KIỂM TRA XEM CẤU HÌNH CÓ ĐƯỢC LƯU THÀNH CÔNG HAY KHÔNG
    try:
        # IN RA MÀN HÌNH
        dylib.print_green("Click vào nút lưu cấu hình")

        # CLICK VÀO NÚT LƯU CẤU HÌNH
        driver.find_element(By.CSS_SELECTOR, "#formLive > button").click()

        # CHO LOAD LẠI TRANG WEB
        driver.refresh()

        # KIỂM TRA XEM TRANG WEB LOAD XONG CHƯA
        # SAU KHI TRANG WEB LOAD XONG THÌ => CẤU HÌNH ĐÃ ĐƯỢC LƯU LẠI
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[1]')))

        # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
        dylib.print_yellow_and_send_message(user_id, "Tạo cấu hình mới thành công")
    except TimeoutError:
        # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
        dylib.print_red_and_send_message(user_id, "Tạo cấu hình mới thất bại")

    sleep(1)

    # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
    dylib.print_yellow_and_send_message(user_id, "Tiến hành mở phiên live")

    # MỞ LIVE
    try:
        dylib.print_green("Click vào nút mở live")

        # CLICK VÀO NÚT MỞ LIVE
        driver.find_element(By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-status='1'][data-toggle='tooltip'][data-placement='top'][data-original-title='Bắt đầu live']").click()

        # ĐỢI THÔNG BÁO THÀNH CÔNG XUẤT HIỆN
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#table-live > tbody > tr > td:nth-child(10) > span')))

        # IN RA MÀN HÌNH VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
        dylib.print_yellow_and_send_message(user_id, "Mở livestream thành công")
    except TimeoutError:
        # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
        dylib.print_red_and_send_message(user_id, "Mở livestream không thành công")
        
        # ĐÓNG CHROME
        driver.quit()

        # KẾT THÚC TIẾN TRÌNH
        return
    
    # IN RA MÀN HÌNH
    dylib.print_yellow("Tiến hành kiểm tra khi nào phiên live được mở")

    # KIỂM TRA XEM PHIÊN LIVE ĐƯỢC MỞ HAY CHƯA
    try:
        # MỞ PHIÊN LIVE
        driver.get(f'https://www.tiktok.com/@{id_tiktok}/live')

        # ĐỢI PHIÊN LIVE LOAD XONG
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[1]/div/div[1]/a')))

        # IN RA MÀN HÌNH VÀ GỬI TIN NHẮN
        dylib.print_green_and_send_message(user_id, "Khi nào phiên live được diễn ra tôi sẽ thông báo cho bạn")
        
        # KIỂM TRA SỐ LƯỢNG NGƯỜI XEM ĐỂ XÁC ĐỊNH PHIÊN LIVE ĐƯỢC MỞ HAY CHƯA
        while True:
            # CHỜ WEB LOAD XONG SAU KHI LÀM MỚI Ở PHẦN EXCEPT BÊN DƯỚI
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[1]/div/div[1]/a')))
            now = datetime.datetime.now()
            try:
                # LẤY DỮ LIỆU CỦA PHẦN TỬ CHỨA SỐ LƯỢNG NGƯỜI XEM CHUYỂN THÀNH VĂN BẢN 
                # VÀ KIỂM TRA DỮ LIỆU BẰNG ĐIỀU KIỆN IF
                element = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div")
                view = element.text

                # NẾU SỐ LƯỢNG NGƯỜI XEM TỪ 0 TRỞ LÊN => PHIÊN LIVE ĐÃ ĐƯỢC MỞ
                if int(view) >= 0:
                    dylib.print_yellow_and_send_message(user_id, f"Phiên live đã được diễn ra vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")
                    driver.quit()
                    break
            # NẾU CHƯA ĐƯỢC DIỄN RA THÌ TIẾP TỤC KIỂM TRA            
            except:
                dylib.print_green(f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live chưa được diễn ra => TIẾP TỤC KIỂM TRA...")
                driver.refresh()
    except:
        # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
        dylib.print_red_and_send_message(user_id, "Kiểm tra thất bại")

        # ĐÓNG CHROME
        driver.quit()

        # KẾT THÚC TIẾN TRÌNH
        return