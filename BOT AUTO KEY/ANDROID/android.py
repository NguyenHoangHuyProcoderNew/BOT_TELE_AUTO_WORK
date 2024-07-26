# IMPORT CÁC THƯ VIỆN CẦN THIẾT
import os
import logging
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import telebot
import pyperclip
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from colorama import Fore, Style, init
from dylib import dylib
import datetime

# CẤU HÌNH WEBDRIVER
chromedriver_path = r'D:\\BOT_TELE_AUTO_WORK\\BOT AUTO KEY\\chrome_driver\\chromedriver.exe'
options = Options()
options.add_argument('--log-level=3')  # Vô hiệu hóa thông báo của Selenium

service = Service(chromedriver_path)
service_log_path = os.path.devnull
service = Service(chromedriver_path, service_log_path=service_log_path)

# KHAI BÁO APT TOKEN BOT TELEGRAM
API_TOKEN = '6555297922:AAF7DFvu9c-gi10-wBtwa_3jKa3TeyInNQ8'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

user_id = '5634845912'  # ID CỦA NGƯỜI DÙNG

timekey = None

# CẤU HÌNH LOGGING
logging.basicConfig(level=logging.CRITICAL)  # Chỉ in thông báo lỗi nghiêm trọng

# CÀI ĐẶT MÀU SẮC
init()

# LẤY THỜI GIAN HIỆN TẠI
now = datetime.datetime.now()

# HÀM YÊU CẦU NGƯỜI DÙNG NHẬP THỜI GIAN SỬ DỤNG CỦA KEY
def ask_user_timekey_android(message):
    green_text = "TẠO KEY ANDROID"
    print(f"\n============= | {Fore.GREEN}{green_text}{Style.RESET_ALL} | =============")

    # YÊU CẦU NGƯỜI DÙNG NHẬP THỜI GIAN SỬ DỤNG KEY
    dylib.bot_reply(user_id, "Vui lòng nhập thời gian sử dụng key\nChỉ được nhập các số nguyên từ 1-30:")
    dylib.print_red("Đang đợi người dùng nhập thời gian sử dụng của key...")

    bot.register_next_step_handler(message, main_create_key_android)

# HÀM CHÍNH XỬ LÝ CÁC TÁC VỤ ĐỂ TẠO KEY
def main_create_key_android(message):
    global timekey
    timekey = int(message.text)

    # XÁC NHẬN THÔNG TIN TẠO KEY
    dylib.bot_reply(user_id, f"Tiến hành tạo: 01 key\nTHÔNG TIN KEY\nThiết bị hỗ trợ: ANDROID\nSố lượng thiết bị sử dụng: 01 thiết bị\nThời gian sử dụng key: {timekey} ngày")
    dylib.print_green(f"Tiến hành tạo 1 key với thời gian sử dụng {timekey} ngày")

    # MỞ WEBSITE TẠO KEY
    dylib.bot_reply(user_id, "Đang mở website tạo key")
    
    # KHỞI TẠO WEB DRIVER
    driver = webdriver.Chrome(service=service, options=options) ; dylib.print_green("KHỞI TẠO WEB DRIVER\n")

    # MỞ WEBSITE
    dylib.print_green("Mở website tạo key")
    driver.get('https://mypanelhuymapsang.000webhostapp.com/login')
    # KIỂM TRA XEM CÓ TRUY CẬP TRANG WEB THÀNH CÔNG HAY KHÔNG
    try:
        dylib.print_green_and_send_message(user_id, "Đang tải website tạo key...")
        WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '/html/body/header/nav/div/a')))
        dylib.print_yellow_and_send_message(user_id, "Tải website tạo key thành công")
    except TimeoutException:
        dylib.print_yellow_and_send_message(user_id, "Có lỗi xảy ra khi truy cập vào website tạo key, vui lòng kiểm tra lại kết nối mạng của máy chủ.")
        driver.quit()
        return

    # ĐĂNG NHẬP VÀO WEB
    dylib.print_red_and_send_message(user_id, "Đang đăng nhập vào web") ; dylib.print_yellow("Đăng nhập vào web tạo key")

    # NHẬP TÀI KHOẢN
    dylib.print_green("Đang nhập tài khoản") ; driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div[2]/form/div[1]/input").send_keys('HUYMAPSANG')
    dylib.print_green("Đang nhập mật khẩu") ; driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div[2]/form/div[2]/input").send_keys('99999999')
    dylib.print_green("Click vào nút đăng nhập") ; driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div[2]/form/div[5]/button").click()

    try:
        WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div[2]/div/div[1]')))
        dylib.print_yellow_and_send_message(user_id, "Đăng nhập thành công")
    except TimeoutException:
        dylib.print_red_and_send_message(user_id, "Có lỗi xảy ra khi đăng nhập vào website tạo key, vui lòng kiểm tra lại kết nối mạng của máy chủ.")
        return

    # TRUY CẬP TRANG TẠO KEY
    dylib.print_green_and_send_message(user_id, "Truy cập vào mục tạo key")
    driver.get('https://mypanelhuymapsang.000webhostapp.com/keys/generate')
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div/div[2]/div[1]/div/div[1]')))
        dylib.print_yellow_and_send_message(user_id, "Truy cập vào mục tạo key thành công")
    except TimeoutException:
        dylib.print_yellow_and_send_message(user_id, "Có lỗi xảy ra khi truy cập vào mục tạo key, vui lòng kiểm tra lại kết nối mạng của máy chủ.")
        driver.quit()
        return

    # XỬ LÝ VIỆC TẠO KEY
    dylib.print_red_and_send_message(user_id, "Tiến hành tạo key")

    # CHỌN THỜI GIAN KEY
    dylib.print_green("Chọn thời gian key") ; dylib.bot_reply(user_id, f"Đang chọn thời gian của key : {timekey} ngày")
    select_day_option = f'#duration > option:nth-child({timekey + 2})'
    driver.find_element(By.CSS_SELECTOR, select_day_option).click()

    # CLICK VÀO NÚT TẠO KEY
    dylib.print_green("Click vào nút TẠO KEY") ; dylib.bot_reply(user_id, "Key đang được tạo...")
    try:
        driver.find_element(By.CSS_SELECTOR, "body > main > div > div > div > div.card > div.card-body > form > div:nth-child(5) > button").click()
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div/div[1]')))
        dylib.print_yellow_and_send_message(user_id, "Tạo key thành công")
    except TimeoutException:
        dylib.print_yellow_and_send_message(user_id, "Tạo key thất bại")
        driver.quit()
        return

    # GỬI KEY CHO NGƯỜI DÙNG
    dylib.print_yellow("Gửi key cho người dùng") ; dylib.bot_reply(user_id, "Key của bạn:")

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert.alert-success')))
        key_data = driver.execute_script("return document.querySelector('.alert.alert-success strong').innerText;")
        dylib.bot_reply(user_id, f"{key_data}") ; dylib.print_red("Gửi key cho người dùng thành công")
        driver.quit()
    except Exception:
        dylib.print_red_and_send_message(user_id, "Tạo key thất bại")
        driver.quit()