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
from dylib import dylib

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

user_id = '6355094590' # ID CỦA NGƯỜI DÙNG

timekey = None

########################### BẮT ĐẦU CÁC CHỨC NĂNG CỦA BOT ###########################


@bot.message_handler(commands=['android'])
def main_create_key_android(message):
    green_text = "TẠO KEY ANDROID"

    print(f"\n============= | {Fore.GREEN}{green_text}{Style.RESET_ALL} | =============")

    msg = bot.send_message(message.chat.id, "Xin vui lòng nhập số ngày sử dụng key:")
    bot.register_next_step_handler(msg, timekey_android)

def timekey_android(message):
    global timekey
    timekey = int(message.text)
    
    # KHỞI TẠO WEB DRIVER
    driver = webdriver.Chrome(service=service, options=options)

    # IN RA MÀN HÌNH
    dylib.print_yellow("KHỞI TẠO WEB DRIVER\n")

    # IN VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
    dylib.print_yellow_and_send_message(user_id, f"Tiến hành tạo: 01 key\nTHÔNG TIN KEY\nThiết bị hỗ trợ: ANDROID\nSố lượng thiết bị sử dụng: 01 thiết bị\nThời gian sử dụng key: {timekey} ngày")

    dylib.print_yellow_and_send_message(user_id, "Vui lòng chờ...")

    # IN RA MÀN HÌNH
    dylib.print_green("Mở website tạo key")
    # MỞ WEBSITE TẠO KEY
    driver.get('https://mypanelhuymapsang.000webhostapp.com/login')

    # KIỂM TRA XEM TRANG WEB LOAD XONG CHƯA
    try:
        # IN RA MÀN HÌNH
        dylib.print_green("Đang tải website tạo key...")

        # ĐỢI PHẦN TỬ CỦA WEBSITE XUẤT HIỆN ĐỂ KIỂM TRA XEM WEB LOAD XONG CHƯA
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/header/nav/div/a')))

        # IN RA MÀN HÌNH
        dylib.print_green("Tải website tạo key thành công")
    except TimeoutError:
        # IN RA MÀN HÌNH VÀ GỬI TIN NHẮN
        dylib.print_red_and_send_message(user_id, "Tạo key thất bại")

    # ĐĂNG NHẬP VÀO WEB
    
    # IN RA MÀN HÌNH
    dylib.print_yellow("Đăng nhập vào web tạo key")

    # IN RA MÀN HÌNH
    dylib.print_green("Nhập tài khoản")

    # NHẬP TÀI KHOẢN
    driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div[2]/form/div[1]/input").send_keys('HUYMAPSANG')

    # IN RA MÀN HÌNH
    dylib.print_green("Nhập mật khẩu")

    # NHẬP MẬT KHẨU
    driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div[2]/form/div[2]/input").send_keys('99999999')

    # IN RA MÀN HÌNH
    dylib.print_green("Click vào nút đăng nhập")

    # CLICK VÀO NÚT ĐĂNG NHẬP
    driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div[2]/form/div[5]/button").click()

    try:
        # KIỂM TRA XEM CÓ ĐĂNG NHẬP THÀNH CÔNG HAY KHÔNG
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div[2]/div/div[1]')))

        # IN RA MÀN HÌNH
        dylib.print_yellow("Đăng nhập thành công")
    except TimeoutError:
        # IN RA MÀN HÌNH VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
        dylib.print_red_and_send_message(user_id, "Tạo key thất bại")

    # IN RA MÀN HÌNH
    dylib.print_yellow("Truy cập trang tạo key")

    # MỞ TRANG TẠO KEY
    driver.get('https://mypanelhuymapsang.000webhostapp.com/keys/generate')

    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div/div[2]/div[1]/div/div[1]')))
        # IN RA MÀN HÌNH
        dylib.print_yellow("Truy cập trang tạo key thành công")
    except TimeoutError:
        # IN RA MÀN HÌNH VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
        dylib.print_red_and_send_message(user_id, "Tạo key thất bại")

    # IN RA MÀN HÌNH
    dylib.print_green("Chọn thời gian key")              

    # CHỌN THỜI GIAN KEY
    select_day_option = f'#duration > option:nth-child({timekey + 2})'
    driver.find_element(By.CSS_SELECTOR, select_day_option).click()

    # IN RA MÀN HÌNH
    dylib.print_green("Click vào nút TẠO KEY")

    try:
        # CLICK VÀO NÚT TẠO KEY
        driver.find_element(By.CSS_SELECTOR, "body > main > div > div > div > div.card > div.card-body > form > div:nth-child(5) > button").click()

        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div/div[1]')))

        # IN RA MÀN HÌNH
        dylib.print_yellow_and_send_message(user_id, "Tạo key thành công")
    except TimeoutError:
        # IN RA MÀN HÌNH VÀ GỬI TIN NHẮN CHO NGƯỜI DÙNG
        dylib.print_red_and_send_message(user_id, "Tạo key thất bại")

    # IN RA MÀN HÌNH
    dylib.print_yellow("Gửi key cho người dùng")

    # IN VÀ GỬI TIN NHẮN
    dylib.print_green_and_send_message(user_id, "Key của bạn:")

    try:
        # Đợi cho đến khi phần tử <div> chứa lớp 'alert alert-success' xuất hiện
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert.alert-success'))
        )
        
        # Sử dụng JavaScript để lấy dữ liệu của phần tử <strong>
        key_data = driver.execute_script("return document.querySelector('.alert.alert-success strong').innerText;")
        
        dylib.print_yellow_and_send_message(user_id, f"{key_data}")
    except Exception as e:
        dylib.print_red_and_send_message(user_id, "Tạo key thất bại")
        driver.quit()
        return

    # IN RA MÀN HÌNH
    dylib.print_yellow("Gửi key cho người dùng thành công")

    driver.quit()    