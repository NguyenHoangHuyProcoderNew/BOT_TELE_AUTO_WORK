# Import các thư viện cần thiết
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
logging.basicConfig(level=logging.CRITICAL)
import datetime
from selenium.common.exceptions import TimeoutException
from colorama import Fore, Style, init
from telebot import types

# BIẾN LẤY NGÀY GIỜ HIỆN TẠI CỦA HỆ THỐNG
now = datetime.datetime.now()

# Đường dẫn đến tệp chromedriver.exe cho Selenium WebDriver
chromedriver_path = r'D:\\BOT_TELE_AUTO_WORK\\BOT LIVE THU CONG\\chrome_driver\\chromedriver.exe'

# Cấu hình chrome driver
options = Options()
options.add_argument('--log-level=3')  # Vô hiệu hóa thông báo của Selenium
options.add_argument('--user-data-dir=D:\\BOT_TELE_AUTO_WORK\\BOT LIVE THU CONG\\du lieu trinh duyet')

service = Service(chromedriver_path)
service_log_path = os.path.devnull
service = Service(chromedriver_path, service_log_path=service_log_path)

# Nhập chức năng bot phản hồi lại người dùng
from dylib.dylib import bot_reply

# Nhập các hàm thực hiện việc in ra màn hình
from print_logger.print_logger import log_info, log_warning, log_error, log_success

# Khai báo API token telegram
API_TOKEN = '7329003333:AAF7GhjivbGnk0jSGE8XfefFh_-shHAFsGc'  # Thay token của bot vào đây
bot = telebot.TeleBot(API_TOKEN)

# Nhập giá trị của user_id ADMIN và user_name của ADMIN từ file dylib trong folder dylib
from dylib.dylib import user_id
from dylib.dylib import username

# Khởi tạo biến ip và device với giá trị mặc định là None
ip = None
device = None

# TRỞ VỀ MENU CHÍNH
@bot.message_handler(func=lambda message: message.text in ["Trở lại menu chính", "Không, trở về menu chính"])
def back_home(message):
    # TẠO NÚT TRỞ VỀ MENU CHÍNH
    button_back_home = telebot.types.ReplyKeyboardMarkup(True).add("Đổi IP").add("Mở live").add("Tắt live").add("Check view")
    text = "VUI LÒNG CHỌN 👇"
    bot.send_message(message.chat.id, text, reply_markup=button_back_home) 

# Hàm yêu cầu người dùng chọn tài khoản cần đổi IP
def ask_select_account_doiip(message):
    # TẠO NÚT CHỌN TÀI KHOẢN CẦN ĐỔI IP
    button_select_account_doiip = telebot.types.ReplyKeyboardMarkup(True).add("Đổi IP Nick Văn Bảo").add("Đổi IP Nick Phụ LBH").add("Đổi IP Nick Meme Lỏ").add("Trở lại menu chính")

    # YÊU CẦU NGƯỜI DÙNG CHỌN TÀI KHOẢN CẦN ĐỔI IP
    log_info(f"Đang đợi người dùng {username} chọn tài khoản cần đổi IP")
    bot.send_message(message.chat.id, "Bạn muốn đổi IP tài khoản nào?", reply_markup=button_select_account_doiip)

    # Chạy hàm doiip
    bot.register_next_step_handler(message, doiip_main)   

def doiip_main(message):
    from dylib.dylib import close_existing_browser # Nhập hàm đóng tất cả các phiên trình duyệt chrome đang chạy
    global ip
    global device

    if message.text == "Đổi IP Nick Văn Bảo":
        ip = "ip-22680"
        device = "renew-22680"
        log_info(f"Người dùng {username} đã chọn Đổi IP Nick Văn Bảo")
        bot_reply(user_id, "Tiến hành đổi IP & Thiết Bị cho Nick Văn Bảo")
    elif message.text == "Đổi IP Nick Phụ LBH":
        ip = "ip-22679"
        device = "renew-22679"
        log_info(f"Người dùng {username} đã chọn Đổi IP Nick Phụ LBH")
        bot_reply(user_id, "Tiến hành đổi IP & Thiết Bị cho Nick Phụ LBH")
    elif message.text == "Đổi IP Nick Meme Lỏ":
        ip = "ip-22733"
        device = "renew-22733"
        log_info(f"Người dùng {username} đã chọn Đổi IP Nick Meme Lỏ")
        bot_reply(user_id, "Tiến hành đổi IP & Thiết Bị cho Nick Meme Lỏ")
    elif message.text == "Trở lại menu chính":
        log_info(f"Người dùng {username} đã chọn Trở Lại Menu Chính")
        back_home(message)
        return

    log_info("Đang chạy hàm kiểm tra các phiên trình duyệt đang chạy, nếu có phiên trình duyệt nào đang được sẽ đóng trình duyệt")
    close_existing_browser() # Đóng tất cả các phiên trình duyệt đang chạy
    # Khởi tạo chrome driver
    driver = webdriver.Chrome(service=service, options=options)
    log_info("Khởi tạo chrome driver")

    try:
        log_info("Mở trang web livestream") ; bot_reply(user_id, "Mở trang web livestream")

        # Mở trang web livestream
        driver.get('https://autolive.me/tiktok')

        log_info("Đang load trang web livestream") ; bot_reply(user_id, "Đang load trang web livestream...")

        # Kiểm tra xem trang web load xong chưa
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))

        log_success("Load trang web livestream thành công") ; bot_reply(user_id, "Load trang web livestream thành công")
    except TimeoutError:
        log_error("Load trang web livestream thất bại") ; bot_reply(user_id, "Load trang web livestream thất bại\nNguyên nhân: đường truyền internet quá yếu hoặc trang web sử dụng băng thông nước ngoài")

        # ĐÓNG CHROME
        driver.quit()
        log_info("Đóng trình duyệt chrome")

        # KẾT THÚC TIẾN TRÌNH
        log_info("Kết thúc tiến trình hiện tại")
        return
    
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

    # Click vào nút Đổi TK Web
    log_info("Click vào nút Đổi TK Web")
    driver.find_element(By.CSS_SELECTOR, "#formLive > div:nth-child(3) > div.col-md-3 > div > div > button:nth-child(2) > i").click()

    # Đợi giao diện sau khi click vào nút Đổi TK Web xuất hiện
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dialog_tiktok > div > div > div")))

    # Biến chứa script thực hiện việc click vào nút đổi IP
    change_ip = f'document.getElementById("{ip}").click();'
    # CLICK VÀO NÚT ĐỔI IP
    driver.execute_script(change_ip)

    bot_reply(user_id, "Đang đổi IP...")
    log_info("Đang đổi IP...")
    # Chờ cho trang web đổi IP
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))

    # Lấy dữ liệu của thông báo web livestream sau khi click vào nút đổi IP
    data_notify_after_changeip = driver.execute_script('''
        // JavaScript code here
        // Đoạn mã JavaScript để lấy nội dung của phần tử
        var element = document.querySelector('div.text[data-notify-html="text"]');
        return element.textContent;
    ''')
    # Kiểm tra xem có đổi IP thành công hay không
    if data_notify_after_changeip == "Thành công":
        log_success("Đổi IP thành công") ; bot_reply(user_id, "Đổi IP thành công")
    else:
        log_error(f"Đổi IP thất bại - Nguyên nhân: {data_notify_after_changeip}")
        bot_reply(user_id, f"Đổi IP thất bại - {data_notify_after_changeip}")

    # Đổi thiết bị
    log_info("Làm mới lại trang web livestream")
    driver.refresh() # Làm mới lại trang web livestream

    # KIỂM TRA SỰ KIỆN TẢI LẠI TRANG CÓ THÀNH CÔNG HAY KHÔNG
    try:
        # Kiểm tra xem trang web load xong chưa
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))

        log_success("Tải lại trang web livestream thành công")

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

    except TimeoutError:
        log_error("Load trang web livestream thất bại")

        # ĐÓNG CHROME
        driver.quit()
        log_info("Đóng trình duyệt chrome")

        # KẾT THÚC TIẾN TRÌNH
        log_info("Kết thúc tiến trình hiện tại")
        return

    # Click vào nút Đổi TK Web
    log_info("Click vào nút Đổi TK Web")
    driver.find_element(By.CSS_SELECTOR, "#formLive > div:nth-child(3) > div.col-md-3 > div > div > button:nth-child(2) > i").click()

    # Đợi giao diện sau khi click vào nút Đổi TK Web xuất hiện
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dialog_tiktok > div > div > div")))

    # Biến chứa script thực hiện việc click vào nút đổi Thiết Bị
    changedevice = f'document.getElementById("{device}").click();'

    log_info("Đang đổi thiết bị...")
    bot_reply(user_id, f"Đang đổi thiết bị...")

    # Click vào nút đổi Thiết Bị
    driver.execute_script(changedevice)

    # Chờ cho trang web đổi Thiết Bị
    WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))

    # Lấy dữ liệu của thông báo web livestream sau khi click vào nút đổi Thiết Bị
    data_notify_after_changedevice = driver.execute_script('''
        // JavaScript code here
        // Đoạn mã JavaScript để lấy nội dung của phần tử
        var element = document.querySelector('div.text[data-notify-html="text"]');
        return element.textContent;
    ''')

    if data_notify_after_changedevice == "Thành công":
        log_success("Đổi Thiết Bị thành công") ; bot_reply(user_id, "Đổi Thiết Bị thành công")

        ask_retry_doiip(message) # Hàm hỏi người dùng có muốn tiếp tục không hoặc về menu chính
        log_info("Đang hỏi người dùng có muốn tiếp tục không hay về menu chính")
        
        log_info("Đóng trình duyệt chrome")
        driver.quit()

        return

    else:
        log_error(f"Đổi Thiết Bị thất bại - Nguyên nhân: {data_notify_after_changedevice}")
        bot_reply(user_id, f"Đổi Thiết Bị thất bại - {data_notify_after_changedevice}")

        ask_retry_doiip(message) # Hàm hỏi người dùng có muốn tiếp tục không hoặc về menu chính
        log_info("Đang hỏi người dùng có muốn tiếp tục không hay về menu chính")

        log_info("Đóng trình duyệt chrome")
        driver.quit()


        return
# Hàm hỏi người dùng tiếp tục hoặc trở lại menu chính
def ask_retry_doiip(message):
    # TẠO NÚT HỎI NGƯỜI DÙNG CÓ MUỐN THỬ LẠI KHÔNG
    button_retry = telebot.types.ReplyKeyboardMarkup(True).add("Có, tiếp tục đổi IP").add("Không, trở về menu chính")
    bot.send_message(message.chat.id, "Bạn có muốn tiếp tục nữa không?", reply_markup=button_retry)