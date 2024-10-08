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
from telebot import types

# Đường dẫn đến chrome driver
chromedriver_path = r'D:\\BOT_TELE_AUTO_WORK\\BOT LIVE THU CONG\\chrome_driver\\chromedriver.exe'

# Cấu hình chrome driver
options = Options()
options.add_argument('--log-level=3')  # Vô hiệu hóa thông báo của Selenium
options.add_argument('--user-data-dir=D:\\BOT_TELE_AUTO_WORK\\BOT LIVE THU CONG\\du lieu trinh duyet')

service = Service(chromedriver_path)
service_log_path = os.path.devnull
service = Service(chromedriver_path, service_log_path=service_log_path)

# KHAI BÁO APT TOKEN BOT TELEGRAM
API_TOKEN = '7329003333:AAF7GhjivbGnk0jSGE8XfefFh_-shHAFsGc'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

# CÁC CHỨC NĂNG IN RA MÀN HÌNH
from print_logger.print_logger import log_info, log_warning, log_error, log_success

# Nhập chức năng bot phản hồi lại người dùng
from dylib.dylib import bot_reply

from dylib.dylib import user_id
from dylib.dylib import username

########## TRỞ VỀ MENU CHÍNH #########
def back_home(message):
    button_menuchinh = telebot.types.ReplyKeyboardMarkup(True).add("Đổi IP").add("Mở live").add("Tắt live").add("Check view")
    bot.send_message(message.chat.id, "VUI LÒNG CHỌN 👇", reply_markup=button_menuchinh)

# Hàm xác nhận tắt live
def xacnhan_tatlive(message):
    # Tạo nút xác nhận tắt live
    xacnhantatlive = telebot.types.ReplyKeyboardMarkup(True)
    xacnhantatlive.add('Có', 'Không').add('Trở lại menu chính')
    bot.send_message(message.chat.id, "Xác nhận tắt phiên live hiện tại?", reply_markup=xacnhantatlive)
    log_info(f"Bot đang yêu cầu người dùng {username} xác nhận tắt phiên live")

    # Sau khi người dùng xác nhận gọi hàm main_tatlive để xử lý
    bot.register_next_step_handler(message, main_tatlive)

# HÀM THỰC HIỆN VIỆC TẮT LIVE
def main_tatlive(message):
    from dylib.dylib import close_existing_browser # Nhập hàm đóng tất cả các phiên trình duyệt chrome đang chạy
    if message.text == "Có":
        log_info("Người dùng đã xác nhận tắt phiên live")

        log_info("Đang chạy hàm kiểm tra các phiên trình duyệt đang chạy, nếu có phiên trình duyệt nào đang được sẽ đóng trình duyệt")
        close_existing_browser() # Đóng tất cả các phiên trình duyệt đang chạy
        log_info("Khởi tạo chrome driver")
        driver = webdriver.Chrome(service=service, options=options)
        
        bot_reply(user_id, "Tiến hành mở trang web livestream")
        log_info("Đang mở trang web livestream")
        driver.get('https://autolive.me/tiktok')

        try:
            bot_reply(user_id, "Đang load trang web livestream...")
            log_info("Đang load trang web livestream")

            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b'))
            )
            
            bot_reply(user_id, "Load trang web livestream thành công")
            log_success("Load trang web livestram thành công")
        except TimeoutError:
            bot_reply(user_id, "Load trang web livestream thất bại, vui lòng kiểm tra lại đường truyền internet")
            log_error("Xảy ra lỗi khi load trang web livestream, do sự cố đường truyền internet")

        bot_reply(user_id, "Tiến hành tắt live")
        log_info("Tiến hành tắt phiên live")

        # try:
        #     log_info("Đang đợi thông báo gia hạn xuất hiện")
        #     # Đợi thông báo gia hạn xuất hiện
        #     WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/div/div/div')))

        #     log_success("Thông báo gia hạn đã xuất hiện")

        #     log_info("Tắt thông báo gia hạn")
        #     driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div/div/div/div[1]/button").click()

        # except TimeoutException:
        #     log_error("Không có thông báo gia hạn")

        # try:
        #     log_info("Đang đợi thông báo gia hạn xuất hiện")
        #     # Đợi thông báo gia hạn xuất hiện
        #     WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[3]/div/div/div')))

        #     log_success("Thông báo gia hạn đã xuất hiện")

        #     log_info("Tắt thông báo gia hạn")
        #     driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[3]/div/div/div/div[1]/button").click()

        # except TimeoutException:
        #     log_error("Không có thông báo gia hạn")
            
        try:
            button_tatlive = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-original-title='Dừng live']"))
            )
            if button_tatlive.get_attribute("data-original-title") == "Dừng live":
                bot_reply(user_id, "Đang tắt phiên live...")
                button_tatlive.click()
                log_info("Click vào nút tắt live")
        except TimeoutException:
            bot_reply(user_id, "Hiện không có phiên live nào được mở")
            log_info("Hiện không có phiên live nào được mở")

            log_info("Đóng trình duyệt chrome")
            driver.quit()

            log_info("Kết thúc tiến trình")
            return

        log_info("Đang kiểm tra có tắt phiên live thành công hay không")

        # # Đợi thông báo sau khi tắt live xuất hiện
        # WebDriverWait(driver, 100).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR, 'div > div.notifyjs-container > div'))
        # )
            
        # log_info("Đang lấy dữ liệu thông báo của web sau khi tắt live")
        # notify_tatlive = driver.find_element(By.CSS_SELECTOR, 'div.text[data-notify-html="text"]')

        # log_info("Đang chuyển dữ liệu thông báo của web sau khi tắt live thành văn bản")
        # data_notify_tatlive = notify_tatlive.text

        # log_info("Đang kiểm tra dữ liệu thông báo của web")
        # if data_notify_tatlive == "Success":
        #     bot_reply(user_id, "Tắt live thành công")
        #     log_success(f"Thông báo của web là {data_notify_tatlive} - Tắt live thành công")

        #     log_info("Đóng trình duyệt chrome")
        #     driver.quit()
        #     log_info("Kết thúc tiến trình")
        # else:
        #     bot_reply(user_id, f"Tắt live không thành công - Thông báo từ trang web: {data_notify_tatlive}")
        #     log_error(f"Tắt live không thành công - Nguyên nhân: {data_notify_tatlive}")

        #     log_info("Đóng trình duyệt chrome")
        #     driver.quit()
        #     log_info("Kết thúc tiến trình")

        # Kiểm tra dữ liệu của phần tử trạng thái để xác định đã tắt live hay chưa
        try:
            # Chờ đợi phần tử Trạng thái xuất hiện
            WebDriverWait(driver, 1000).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.badge.badge-success"))
            )
            
            # Chờ đến khi giá trị của phần tử là "Mới"
            check_data_phantutrangthai = WebDriverWait(driver, 1000).until(
                lambda d: d.execute_script(
                    "return document.querySelector('span.badge.badge-success').textContent;"
                ) == "Mới"
            )

            bot_reply(user_id, "Tắt live thành công")
            log_success(f"Tắt live thành công - Dữ liệu của phần tử Trạng thái là: {check_data_phantutrangthai}")
        except TimeoutException:
            log_error("Tắt live không thành công")
            bot_reply(user_id, "Tắt live không thành công")

            driver.quit()
            log_info("Đóng trình duyệt chrome")

            log_info("Kết thúc tiến trình")
            return

    elif message.text in ["Không", "Trở lại menu chính"]:
        back_home(message)
