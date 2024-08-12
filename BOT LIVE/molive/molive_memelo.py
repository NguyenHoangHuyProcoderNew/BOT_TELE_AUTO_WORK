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

# THÔNG TIN TÀI KHOẢN LIVE
id_tiktok = "meme.l810"
select_account = "#tiktok_account > option:nth-child(4)"

# Link nguồn
linknguon = None

# Trở về menu chính
home = telebot.types.ReplyKeyboardMarkup(True).add("Đổi IP").add("Mở live").add("Tắt live").add("Check view")
def back_home(message):
    text = "VUI LÒNG CHỌN 👇"
    bot.send_message(message.chat.id, text, reply_markup=home)

# Hàm yêu cầu người dùng chọn nguồn cho phiên live
def ask_source_live_memelo(message):
    # Tạo nút chọn nguồn cho phiên live
    button_select_source_live = types.ReplyKeyboardMarkup(True).add('HỒI CHIÊU').add('QUỲNH EM').add('Trở lại menu chính')
    bot.send_message(message.chat.id, "Bạn muốn sử dụng nguồn live nào cho phiên live?", reply_markup=button_select_source_live)
    log_info("Đang yêu cầu người dùng chọn nguồn cho phiên live")
    
    bot.register_next_step_handler(message, main_molive_memelo)

# Hàm thực hiện việc mở phiên live
def main_molive_memelo(message):
    from dylib.dylib import close_existing_browser # Nhập hàm đóng tất cả các phiên trình duyệt chrome đang chạy
    global linknguon

    if message.text == "HỒI CHIÊU":
        linknguon = "https://drive.google.com/file/d/1PrRqUCTGm0nseYKJwARZYuCmsxMc-T7k/view?usp=drivesdk" # NGUỒN HỒI CHIÊU
        bot_reply(user_id, "Tiến hành mở phiên live với nguồn HỒI CHIÊU")
        log_info(f"Người dùng {username} đã chọn nguồn live HỒI CHIÊU")
    elif message.text == "QUỲNH EM":
        linknguon = "https://drive.google.com/file/d/1QEX0hXjZZEvY6IjAaBzP7hhuzRop05Gz/view?usp=sharing" # NGUỒN QUỲNH EM
        bot_reply(user_id, "Tiến hành mở phiên live với nguồn QUỲNH EM")
        log_info("Tiến hành mở phiên live với nguồn QUỲNH EM")
    elif message.text == "Trở lại menu chính":
        log_info(f"Người dùng {username} đã chọn Trở lại menu chính")
        back_home(message)
        return

    log_info("Đang chạy hàm kiểm tra các phiên trình duyệt đang chạy, nếu có phiên trình duyệt nào đang được sẽ đóng trình duyệt")
    close_existing_browser() # Đóng tất cả các phiên trình duyệt đang chạy
    # Khởi tạo chrome driver
    driver = webdriver.Chrome(service=service, options=options)
    log_info("Khởi tạo chrome driver")

    try:
        # Mở trang web livestream
        bot_reply(user_id, "Đang mở trang web livestream")
        log_info("Mở trang web livestream")
        driver.get('https://autolive.me/tiktok')
        
        bot_reply(user_id, "Đang load trang web livestream...")
        log_info("Đang load trang web livestream")

        # Kiểm tra xem trang web đã load xong chưa
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))

        bot_reply(user_id, "Load trang web livestream thành công")
        log_success("Load trang web livestream thành công")
    except TimeoutError:
        bot_reply(user_id, "Load trang web livestream thất bại\nNguyên nhân: đường truyền internet quá yếu hoặc trang web sử dụng băng thông nước ngoài dẫn đến lỗi, kiểm tra lại kết nối internet của máy chủ")
        log_error("Load trang web livestream thất bại")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return

    try:
        log_info("Đang đợi thông báo gia hạn xuất hiện")
        # Đợi thông báo gia hạn xuất hiện
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[3]/div/div/div')))

        log_success("Thông báo gia hạn đã xuất hiện")

        log_info("Tắt thông báo gia hạn")
        driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[3]/div/div/div/div[1]/button").click()

    except TimeoutException:
        log_error("Không có thông báo gia hạn")

    # XÓA CẤU HÌNH CŨ
    bot_reply(user_id, "Tiến hành xóa cấu hình cũ")
    log_info("Xóa cấu hình cũ")
    try:
        log_info("Click vào nút xóa cấu hình")
        driver.find_element(By.XPATH, '//button[@class="btn btn-circle btn-dark btn-sm waves-effect waves-light btn-status-live" and @data-status="-1" and @data-toggle="tooltip"]').click()

        log_info("Đang đợi thông báo của web sau khi xóa cấu hình cũ...")

        # Đợi thông báo sau khi xóa cấu hình cũ xuất hiện
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))

        # Lấy dữ liệu của thông báo xóa cấu hình cũ
        log_info("Thông báo của web sau khi xóa cấu hình cũ đã xuất hiện, đang lấy dữ liệu của thông báo...")
        notify_xoacauhinh = driver.find_element(By.CSS_SELECTOR, 'div.text[data-notify-html="text"]')

        # Chuyển dữ liệu của thông báo xóa cấu hình cũ thành văn bản
        log_info("Đang chuyển dữ liệu của thông báo thành văn bản...")
        data_notify_xoacauhinh = notify_xoacauhinh.text

        # KIỂM TRA DỮ LIỆU CỦA THÔNG BÁO
        log_info("Đang kiểm tra dữ liệu của thông báo")
        if data_notify_xoacauhinh == "Bạn phải dừng luồng live trước khi xóa":
            bot_reply(user_id, "Hiện đang có 1 luồng live đang được mở, vui lòng dừng luồng live rồi thử lại")
            log_error(f"Không thể xóa cấu hình cũ - Thông báo từ web: {data_notify_xoacauhinh}")
            
            log_info("Đóng trình duyệt chrome")
            driver.quit()

            log_info("Kết thúc tiến trình")
            return
        else:
            bot_reply(user_id, "Xóa cấu hình thành công")
            log_info("Xóa cấu hình thành công")
    except NoSuchElementException:
        bot_reply(user_id, "Hiện tại không có cấu hình cũ nào")
        log_info("Hiện tại không có cấu hình")

    # TẠO CẤU HÌNH MỚI
    bot_reply(user_id, "Tiến hành tạo cấu hình mới")
    log_info("Tạo cấu hình live mới")

    # CHỌN TÀI KHOẢN LIVE
    log_info("Đang chọn tài khoản live")
    driver.find_element(By.CSS_SELECTOR, f"{select_account}").click()

    # NHẬP TIÊU ĐỀ LIVE
    log_info("Đang nhập tiêu đề live")
    driver.find_element(By.ID, "title").send_keys('kéo rank Liên Quân')

    # CHỌN CHỦ ĐỀ LIVE
    log_info("Đang chọn chủ đề live")
    driver.find_element(By.CSS_SELECTOR, "#topic > option:nth-child(11)").click()

    # CHỌN KIỂU LIVE
    log_info("Đang chọn kiểu live")
    driver.find_element(By.CSS_SELECTOR, "#formLive > div:nth-child(6) > div > div > div > button:nth-child(2) > i").click()

    # NHẬP LINK NGUỒN
    log_info("Đang nhập link nguồn cho phiên live")
    driver.find_element(By.ID, "url_source").send_keys(linknguon)

    # LƯU CẤU HÌNH
    log_info("Cấu hình hoàn tất, tiến hành lưu lại cấu hình")

    try:
        log_info("Click vào nút lưu cấu hình")
        driver.find_element(By.CSS_SELECTOR, "#formLive > button").click()

        log_info("Làm mới lại trang web")
        driver.refresh()

        log_info("Đang làm mới lại trang web để lưu cấu hình...")
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[1]')))

        bot_reply(user_id, "Tạo cấu hình mới hoàn tất")
        log_info("Lưu cấu hình thành công")

        try:
            log_info("Đang đợi thông báo gia hạn xuất hiện")
            # Đợi thông báo gia hạn xuất hiện
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[3]/div/div/div')))

            log_success("Thông báo gia hạn đã xuất hiện")

            log_info("Tắt thông báo gia hạn")
            driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[3]/div/div/div/div[1]/button").click()

        except TimeoutException:
            log_error("Không có thông báo gia hạn")
    except TimeoutError:
        bot_reply(user_id, "Tạo cấu hình mới thất bại")
        log_info("Tạo cấu hình mới thất bại")

    bot_reply(user_id, "Đang mở live...")
    log_info("Tiến hành mở phiên live")

    try:
        log_info("Click vào nút mở phiên live")
        driver.find_element(By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-status='1'][data-toggle='tooltip'][data-placement='top'][data-original-title='Bắt đầu live']").click()

        log_info("Đang đợi thông báo của web sau khi click vào nút mở phiên live xuất hiện")
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))

        log_info("Đang lấy dữ liệu của thông báo của web sau khi mở phiên live")
        notify_openlive = driver.execute_script('''
        // JavaScript code here
        // Đoạn mã JavaScript để lấy nội dung của phần tử
        var element = document.querySelector('div.text[data-notify-html="text"]');
        return element.textContent;
    ''')
        
        if notify_openlive == "Success":
            bot_reply(user_id, "Mở phiên live thành công")
            log_info(f"Thông báo của web là {notify_openlive} - Mở live thành công")
        else:
            bot_reply(user_id, f"Mở phiên live thất bại\nThông báo từ web: {notify_openlive}")
            log_error(f"Mở phiên live thất bại - Thông báo từ web: {notify_openlive}")
    except TimeoutError:
        bot_reply(user_id, "Mở phiên live thất bại\nNguyên nhân: sự cố kết nối từ máy chủ")
        log_error("Không thể mở phiên live - Sự cố kết nối từ máy chủ")
    
    
    bot_reply(user_id, "Tiến hành kiểm tra khi nào phiên live được mở")
    log_info("Tiến hành kiểm tra thời điểm phiên live diễn ra")
    try:
        bot_reply(user_id, "Đang truy cập vào phiên live")
        log_info("Đang mở phiên live")
        driver.get(f'https://www.tiktok.com/@{id_tiktok}/live')

        log_info("Đang load phiên live")
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[3]/div/div[1]/a')))

        bot_reply(user_id, "Truy cập phiên live thành công, khi nào phiên live diễn ra tôi sẽ thông báo cho bạn")
    except TimeoutException:
        bot_reply(user_id, "Không thể truy cập phiên live, xảy ra sự cố kết nối internet")
        log_info("Không thể truy cập phiên live do kết nối internet")

        log_info("Đóng trình duyệt chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return
    
    # HÀM KIỂM TRA PHIÊN LIVE
    while True:
        now = datetime.datetime.now() # Biến lấy ngày giờ hiện tại của hệ thống
        try:
            log_info("Đang check view...")
            checkview = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))
            
            bot_reply(user_id, f"Check live hoàn tất, phiên live đã được mở vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")
            log_info(f"Phiên live đã được diễn ra vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")

            log_info("Đóng trình duyệt chrome")
            driver.quit()

            log_info("Kết thúc tiến trình")
            return
        except TimeoutException:
            log_info("Phiên live chưa được diễn ra")

            log_info("Làm mới lại phiên live")
            driver.refresh()

            # Kiểm tra xem có làm mới lại phiên live thành công hay không
            try:
                WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div[3]/div/div[1]/a"))
                )
            except TimeoutException:
                bot_reply(user_id, "Kiểm tra phiên live thất bại do có sự cố kết nối internet, vui lòng kiểm tra lại đường truyền")
                log_error("Kiểm tra phiên live thất bại do có sự cố về kết nối internet")

                log_info("Đóng trình duyệt chrome")
                driver.quit()

                log_info("Kết thúc tiến trình")
                return