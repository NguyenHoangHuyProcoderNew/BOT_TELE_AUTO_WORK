# Import các thư viện cần thiết
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import telebot

# Cấu hình đường dẫn đến ChromeDriver
CHROMEDRIVER_PATH = r'/Users/macx/Downloads/BOT_TELE_AUTO_WORK-master/BOT KEY/chrome_driver/chromedriver'
API_TOKEN = '7371036517:AAEB8PtQRtSrvDOxQUUW2su7ObGso6ltq8w'  # Token của BOT
bot = telebot.TeleBot(API_TOKEN)

# Nhập các chức năng in log tuỳ chỉnh
from print_logger.print_logger import log_info, log_warning, log_error, log_success

# Nhập chức năng bot phản hồi và thông tin người dùng
from dylib.dylib import bot_reply, user_id

# Cấu hình tùy chọn Chrome cho Selenium
options = Options()
options.add_argument('--log-level=3')  # Giảm thiểu log từ trình duyệt
service = Service(CHROMEDRIVER_PATH)

# Biến toàn cục để lưu thời gian của key
thoigian_key = None

# Yêu cầu người dùng nhập thời gian của key
def nhap_thoigian_key(message):
    bot_reply(user_id, "Vui lòng nhập thời gian của key\nThời gian của key phải là số nguyên từ 1-30:")
    log_info("Bot yêu cầu người dùng nhập thời gian của key.")

    bot.register_next_step_handler(message, xuly_taokey_android)

# Xử lý quá trình tạo key
def xuly_taokey_android(message):
    global thoigian_key
    thoigian_key = int(message.text)

    # Kiểm tra dữ liệu thời gian của key mà người dùng nhập có hợp lệ không
    # thoigian_key = int(message.text)
    if isinstance(thoigian_key, int) and thoigian_key >= 1 and thoigian_key <= 30:
        bot_reply(user_id, f"Tiến hành tạo: 01 key\nThiết bị hỗ trợ: ANDROID\nThời gian sử dụng: {thoigian_key} ngày")
        log_info(f"Tiến hành tạo 1 key với thời gian {thoigian_key} ngày")
    else:
        bot_reply(user_id, "Dữ liệu của key không hợp lệ, bạn chỉ có thể nhập các số nguyên từ 1-30.")
        log_error("Không thể tạo key, do người dùng nhập thời gian key không hợp lệ")

        log_info("Kết thúc tiến trình")
        return

    bot_reply(user_id, "Tiến hành mở trang web tạo key")

    # Khởi tạo Chrome driver
    log_info("Khởi tạo Chrome driver.")
    driver = webdriver.Chrome(service=service, options=options)

    # Mở trang web tạo key
    log_info("Mở trang tạo key")
    driver.get('https://mypanelhuymapsang.000webhostapp.com/login')

    # Kiểm tra xem có truy cập trang tạo key thành công hay không
    try:
        WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '/html/body/header/nav/div/a')))

        bot_reply(user_id, "Mở trang web tạo key thành công")
        log_success("Mở trang tạo key thành công")
    except TimeoutException:
        bot_reply(user_id, "Mở trang web tạo key không thành công, xảy ra sự cố kết nối internet")
        log_error("Mở trang web tạo key không thành công, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt Chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return

    # Đăng nhập vào trang tạo key
    bot_reply(user_id, "Đăng nhập vào web...")
    log_info("Tiến hành đăng nhập")

    log_info("Đang nhập tài khoản")
    driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div[2]/form/div[1]/input").send_keys('HUYMAPSANG')

    log_info("Đang nhập mật khẩu")
    driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div[2]/form/div[2]/input").send_keys('99999999')

    log_info("Click vào nút đăng nhập")
    driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[2]/div[2]/form/div[5]/button").click()

    # Kiểm tra xem có đăng nhập thành công hay không
    try:
        WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div[2]/div/div[1]')))

        bot_reply(user_id, "Đăng nhập thành công")
        log_success("Đăng nhập thành công")
    except TimeoutError:
        bot_reply(user_id, "Đăng nhập thất bại, xảy ra sự cố kết nối internet")
        log_error("Đăng nhập thất bại, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt Chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return

    bot_reply(user_id, "Đang mở trang để tạo key")
    log_info("Mở trang để tạo key")

    # Truy cập vào trang để tạo key
    driver.get('https://mypanelhuymapsang.000webhostapp.com/keys/generate')

    # Kiểm tra xem có truy cập trang để tạo key thành công hay không
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div/div[2]/div[1]/div/div[1]')))

        bot_reply(user_id, "Mở trang để tạo key thành công")
        bot_reply(user_id, "Tiến hành tạo key...")

        log_success("Mở trang để tạo key thành công")
    except TimeoutError:
        bot_reply(user_id, "Mở trang để tạo key thất bại, xảy ra sự cố kết nối internet")
        log_error("Mở trang để tạo key thất bại, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt Chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return

    # Tạo key
    log_info("Chọn thời gian key")
    chon_thoigian_key = f'#duration > option:nth-child({thoigian_key + 2})'
    # Click để chọn thời gian key
    driver.find_element(By.CSS_SELECTOR, chon_thoigian_key).click()

    # Click vào nút tạo key
    log_info("Click vào nút tạo key")
    driver.find_element(By.CSS_SELECTOR, "body > main > div > div > div > div.card > div.card-body > form > div:nth-child(5) > button").click()

    # Kiểm tra xem có tạo key thành công hay không
    try:
        WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div/div/div/div[1]')))

        bot_reply(user_id, "Tạo key thành công")
        log_success("Tạo key thành công")
    except TimeoutError:
        bot_reply(user_id, "Tạo key thất bại, xảy ra sự cố kết nối internet")
        log_error("Tạo key thất bại, xảy ra sự cố kết nối internet")

        log_info("Đóng trình duyệt Chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
        return
    
    log_info("Đang lấy dữ liệu của mã key đã tạo")

    # Đợi phần tử chứa mã key xuất hiện
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert.alert-success')))

        key = driver.execute_script("return document.querySelector('.alert.alert-success strong').innerText;")

        bot_reply(user_id, "Key của bạn là:")
        bot_reply(user_id, f"{key}")

        log_info("Gửi key cho người dùng thành công")
    except TimeoutException:
        bot_reply(user_id, "Không lấy được mã key đã tạo, xảy ra sự cố kết nối internet")
        log_error("Không lấy được dữ liệu của mã key đã tạo, xảy ra sự cố kết nối internet")
    finally:
        log_info("Đóng trình duyệt Chrome")
        driver.quit()

        log_info("Kết thúc tiến trình")
