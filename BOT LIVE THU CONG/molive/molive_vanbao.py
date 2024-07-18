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
ten_tai_khoan = "VĂN BẢO"
id_tiktok = "vanbao165201"
select_account = "#tiktok_account > option:nth-child(3)"

# LINK NGUỒN CHO PHIÊN LIVE 
from nguonlive.linknguon import linknguon

# Khởi tạo colorama
init()

linknguon = None
############################ CHỨC NĂNG CHÍNH ##########################
def main_molive_vanbao(message):
    # IN RA MÀN HÌNH
    print(f"\n============= MỞ LIVE TÀI KHOẢN | {Fore.GREEN}{ten_tai_khoan}{Style.RESET_ALL} | ID Tiktok: {id_tiktok} =============")

    # GỬI TIN NHẮN CHO NGƯỜI DÙNG
    dylib.bot_reply(user_id, f"THỰC THI LỆNH MỞ LIVE TÀI KHOẢN {ten_tai_khoan} THÀNH CÔNG") ; sleep(1)

    # YÊU CẦU NGƯỜI DÙNG LỰA CHỌN NGUỒN CHO PHIÊN LIVE
    dylib.print_yellow("Bot đang yêu cầu người dùng lựa chọn nguồn cho phiên live") ; bot.send_message(message.chat.id, "Xin vui lòng chọn nguồn cho phiên live\n1. Hồi chiêu full HD\n2.Quỳnh em chửi\nVui lòng nhập số 1 hoặc 2 để chọn")

    bot.register_next_step_handler(message, nhaplinknguon)

# hàm xử lý việc lựa chọn nguồn và mở live
def nhaplinknguon(message):
    global linknguon
    nhaplinknguon = message.text
    
    if int(nhaplinknguon) == 1:
        dylib.bot_reply(user_id, "Lựa chọn link nguồn cho phiên live thành công, tiến hành mở phiên live với nguồn | HỒI CHIÊU FULL HD | ") ; dylib.print_green("Người dùng đã chọn 1 => TIẾN HÀNH MỞ LIVE VỚI NGUỒN LIVE | HỒI CHIÊU FULL HD |")
        linknguon = "https://drive.google.com/file/d/1PrRqUCTGm0nseYKJwARZYuCmsxMc-T7k/view?usp=drivesdk"
    elif int(nhaplinknguon) == 2:
        dylib.bot_reply(user_id, "Lựa chọn link nguồn cho phiên live thành công, tiến hành mở phiên live với nguồn | QUỲNH EM CHỬI | ") ; dylib.print_green("Người dùng đã chọn 2 => TIẾN HÀNH MỞ LIVE VỚI NGUỒN LIVE | QUỲNH EM CHỬI |")
        linknguon = "https://drive.google.com/file/d/1QEX0hXjZZEvY6IjAaBzP7hhuzRop05Gz/view?usp=sharing"

    # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
    dylib.print_green_and_send_message(user_id,"Mở trang web livestream")

    # KHỞI TẠO WEB DRIVER
    driver = webdriver.Chrome(service=service, options=options) ; dylib.print_red("KHỞI TẠO WEB DRIVER\n")

    # MỞ WEB LIVESTREAM
    driver.get('https://autolive.me/tiktok')

    # KIỂM TRA XEM TRANG WEB LOAD XONG CHƯA
    try:
        # IN RA MÀN HÌNH
        dylib.print_green_and_send_message(user_id, "Đang load website LIVESTREAM...")

        # ĐỢI PHẦN TỬ CỦA WEB XUẤT HIỆN
        # SAU KHI PHẦN TỬ XUẤT HIỆN => GỬI TIN NHẮN CHO NGƯỜI DÙNG VÀ IN RA MÀN HÌNH ĐỂ THÔNG BÁO
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b'))) ; dylib.print_yellow_and_send_message(user_id, "Load website livestream thành công")
    except TimeoutError:
        # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG NẾU THẤT BẠI
        dylib.print_green_and_send_message(user_id, "Có lỗi xảy ra khi truy cập vào website LIVESTREAM, vui lòng kiểm tra lại kết nối internet của máy chủ.")

        # ĐÓNG CHROME
        driver.quit()

        # KẾT THÚC TIẾN TRÌNH
        return

    # THÔNG BÁO XÓA CẤU HÌNH HIỆN TẠI
    dylib.print_red_and_send_message(user_id, "Tiến hành xóa cấu hình cũ")

    # XÓA CẤU HÌNH CŨ
    try:
        # CLICK VÀO NÚT XÓA CẤU HÌNH
        driver.find_element(By.XPATH, '//button[@class="btn btn-circle btn-dark btn-sm waves-effect waves-light btn-status-live" and @data-status="-1" and @data-toggle="tooltip"]').click() ; dylib.print_green("Click vào nút xóa cấu hình")

        # ĐỢI CẤU HÌNH ĐƯỢC XÓA
        dylib.print_green_and_send_message(user_id, "Đang đợi cấu hình được xóa...") ; WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))

        # KIỂM TRA DỮ LIỆU CỦA THÔNG BÁO KHI CLICK VÀO NÚT XÓA CẤU HÌNH
        # LẤY DỮ LIỆU CỦA THÔNG BÁO XÓA CẤU HÌNH
        check_xoacauhinh = driver.find_element(By.CSS_SELECTOR, 'div.text[data-notify-html="text"]')

        # CHUYỂN DỮ LIỆU CHECK ĐƯỢC THÀNH VĂN BẢN
        data_xoacauhinh = check_xoacauhinh.text

        # KIỂM TRA DỮ LIỆU CỦA THÔNG BÁO
        if data_xoacauhinh == "Bạn phải dừng luồng live trước khi xóa":
            dylib.print_yellow_and_send_message(user_id, "Không thể xóa cấu hình vì có 1 luồng live đang được chạy, vui lòng dừng live bằng lệnh /tatlive rồi thử lại sau")

            # ĐÓNG CHROME
            driver.quit()

            # DỪNG TIẾN TRÌNH
            return
        else:
            dylib.print_yellow_and_send_message(user_id, "Xóa cấu hình thành công")
    except NoSuchElementException:
        # IN RA MÀN HÌNH VÀ GỬI TIN NHẮN
        dylib.print_yellow_and_send_message(user_id, "Hiện tại không có cấu hình")

    # TẠO CẤU HÌNH MỚI
    dylib.print_red_and_send_message(user_id, "Tạo cấu hình mới")

    # CHỌN TÀI KHOẢN LIVE
    dylib.print_green("Chọn tài khoản") ; driver.find_element(By.CSS_SELECTOR, f"{select_account}").click()

    # NHẬP TIÊU ĐỀ LIVE
    dylib.print_green("Nhập tiêu đề live") ; driver.find_element(By.ID, "title").send_keys('kéo rank Liên Quân')

    # CHỌN CHỦ ĐỀ LIVE
    dylib.print_green("Chọn chủ đề live") ; driver.find_element(By.CSS_SELECTOR, "#topic > option:nth-child(11)").click()

    # CHỌN KIỂU LIVE
    dylib.print_green("Chọn kiểu live Mobile") ; driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div/div[3]/div/div/div[2]/form/div[4]/div/div/div/button[2]").click()

    # NHẬP LINK NGUỒN
    dylib.print_green("Nhập link nguồn cho phiên live") ; driver.find_element(By.ID, "url_source").send_keys(linknguon)

    # LƯU CẤU HÌNH
    dylib.print_green("Lưu cấu hình")

    # KIỂM TRA XEM CẤU HÌNH CÓ ĐƯỢC LƯU THÀNH CÔNG HAY KHÔNG
    try:
        # CLICK VÀO NÚT LƯU CẤU HÌNH
        dylib.print_green("Click vào nút lưu cấu hình") ; driver.find_element(By.CSS_SELECTOR, "#formLive > button").click()

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
    dylib.print_yellow_and_send_message(user_id, "Tiến hành mở live")

    # MỞ LIVE
    try:
        dylib.print_green("Click vào nút mở live")

        # CLICK VÀO NÚT MỞ LIVE
        driver.find_element(By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-status='1'][data-toggle='tooltip'][data-placement='top'][data-original-title='Bắt đầu live']").click()

        # ĐỢI THÔNG BÁO THÀNH CÔNG XUẤT HIỆN
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#table-live > tbody > tr > td:nth-child(10) > span')))

        # IN RA MÀN HÌNH VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
        dylib.print_yellow_and_send_message(user_id, "Mở live thành công")
    except TimeoutError:
        # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
        dylib.print_red_and_send_message(user_id, "Mở live không thành công")
        
        # ĐÓNG CHROME
        driver.quit()

        # KẾT THÚC TIẾN TRÌNH
        return
    
    # IN RA MÀN HÌNH
    dylib.print_red("Truy cập vào phiên live để kiểm tra khi nào phiên live được mở")
    # KIỂM TRA XEM PHIÊN LIVE ĐƯỢC MỞ HAY CHƯA
    try:
        # IN RA MÀN HÌNH
        dylib.print_green("Mở phiên live")
        
        # MỞ PHIÊN LIVE
        driver.get(f'https://www.tiktok.com/@{id_tiktok}/live')

        # ĐỢI PHIÊN LIVE LOAD HOÀN TẤT
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div[1]/a')))

        # GỬI TIN NHẮN CHO NGƯỜI DÙNG
        dylib.bot_reply(user_id, "Khi nào phiên live được diễn ra tôi sẽ thông báo cho bạn")

        # IN RA MÀN HÌNH
        dylib.print_yellow("Truy cập phiên live thành công, tiến hành kiểm tra")
    except TimeoutException:
        # IN RA MÀN HÌNH
        dylib.print_yellow_and_send_message(user_id, "Xảy ra sự cố khi truy cập phiên live, vui lòng kiểm tra lại kết nối internet")

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