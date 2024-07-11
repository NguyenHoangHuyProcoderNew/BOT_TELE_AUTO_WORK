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
# CẤU HÌNH LOGGING
logging.basicConfig(level=logging.CRITICAL)  # Chỉ in thông báo lỗi nghiêm trọng
import datetime
now = datetime.datetime.now()
from selenium.common.exceptions import TimeoutException

# ###################### CÁC LINK NGUỒN CHO PHIÊN LIVE ######################
# linknguon = "https://drive.google.com/file/d/1PrRqUCTGm0nseYKJwARZYuCmsxMc-T7k/view?usp=drivesdk" # HỒI CHIÊU FULL HD
# linknguon = "https://www.tiktok.com/@trumkeoranknammod/live" # KÊNH CHÍNH NAMMOD
linknguon = "https://drive.google.com/file/d/1QEX0hXjZZEvY6IjAaBzP7hhuzRop05Gz/view?usp=sharing" # QUỲNH EM CHỬI
# linknguon = "https://www.tiktok.com/@iam_huyle/live" #KÊNH CHÍNH LBH
# linknguon = "https://drive.google.com/file/d/1hRicFqWHyAB_Gvt0LA3BmUPt8VVk3AMd/view?usp=sharing" # quynh em chui + hoi chieu full hd

# CẤU HÌNH WEBDRIVER
chromedriver_path = r'D:\\BOT_TELE_AUTO_WORK\\driver\\chromedriver.exe'

options = Options()
options.add_argument('--log-level=3')  # Vô hiệu hóa thông báo của Selenium
options.add_argument('--user-data-dir=D:\\BOT_TELE_AUTO_WORK\\tk')

service = Service(chromedriver_path)
service_log_path = os.path.devnull
service = Service(chromedriver_path, service_log_path=service_log_path)
# KẾT THÚC CẤU HÌNH WEBDRIVER

# KHAI BÁO APT TOKEN BOT TELEGRAM
API_TOKEN = '7329003333:AAF7GhjivbGnk0jSGE8XfefFh_-shHAFsGc'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

# HÀM NÀY SẼ VỪA CHO BOT GỬI TIN NHẮN VỀ NGƯỜI DÙNG VÀ VỪA IN RA MÀN HÌNH
def bot_reply_and_print(message, text):
    print(text)
    bot.reply_to(message, text)

def countdown(minutes):
    total_seconds = minutes * 60
    for i in range(total_seconds, 0, -1):
        minutes, seconds = divmod(i, 60)
        print(f"Còn {minutes} phút {seconds} giây nữa sẽ tiến hành kiểm tra phiên live.")
        time.sleep(1)
    print("Đếm ngược hoàn tất, tiến hành kiểm tra trạng thái phiên live")


####################### BẮT ĐẦU MÃ CHỨC NĂNG TẮT LIVE #################################
def tatlive(message):

    # KHỞI TẠO WEBDRIVER
    driver = webdriver.Chrome(service=service, options=options)

    bot_reply_and_print(message, "Thực thi lệnh tắt live thành công")

    sleep(1)

    bot_reply_and_print(message, "Tiến hành truy cập vào web live")

#### MỞ WEB LIVE VÀ KIỂM TRA XEM PHIÊN LIVE ĐÃ ĐƯỢC MỞ THÀNH CÔNG HAY CHƯA ###

    # MỞ WEB LIVE
    driver.get('https://autolive.me/tiktok')

    # KIỂM TRA XEM WEBSITE ĐÃ LOAD XONG HAY CHƯA
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))
        bot_reply_and_print(message, "Truy cập vào web live thành công")
    except TimeoutException:
        bot_reply_and_print(message, "Truy cập vào web live thất bại, vui lòng kiểm tra lại kết nối internet và thử lại sau")
        driver.quit()
        return
    
    ################################ TẮT LIVE #################################

    bot_reply_and_print(message, "Tiến hành tắt live")

    button_tatlive = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-original-title='Dừng live']")
    # Kiểm tra giá trị data-original-title của button (Nếu là Dừng live thì mới click)
    if button_tatlive.get_attribute("data-original-title") == "Dừng live":
        button_tatlive.click() # CLICK VÀO NÚT TẮT LIVE NẾU GIÁ TRỊ HỢP LỆ

    else:
        bot_reply_and_print(message, "Hiện tại không có phiên live nào được mở")
        driver.quit()
        return

    # KIỂM TRA SỰ KIỆN TẮT LIVE CÓ THÀNH CÔNG HAY KHÔNG
    try:
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div > div.notifyjs-container > div'))) # ĐỢI THÔNG BÁO TẮT LIVE THÀNH CÔNG XUẤT HIỆN
        bot_reply_and_print(message, "TẮT LIVE THÀNH CÔNG")
        driver.quit()
    except TimeoutException:
        bot_reply_and_print(message, "TẮT LIVE KHÔNG THÀNH CÔNG, VUI LÒNG KIỂM TRA LẠI")
        driver.quit()
        return
####################### KẾT THÚC MÃ CHỨC NĂNG TẮT LIVE ###################


@bot.message_handler(commands=['molive_nickphulbh'])
def molive_nickphulbh(message):

    driver = webdriver.Chrome(service=service, options=options) # Khởi tạo webdriver
    print("Khởi tạo WEBDRIVER")        

    bot_reply_and_print(message, "Thực thi lệnh thành công")
    sleep(1)
    
    bot_reply_and_print(message, "Mở web LIVE")
    sleep(1)

    bot_reply_and_print(message, "Đang tải trang web...")
    sleep(1)

    # MỞ TRANG WEB LIVE VÀ KIỂM TRA XEM TRANG WEB LOAD THÀNH CÔNG HAY CHƯA
    try:
        driver.get('https://autolive.me/tiktok') #MỞ WEB                      

        # KIỂM TRA XEM TRANG WEB ĐÃ LOAD XONG HAY CHƯA
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[1]')))
        
        # GỬI THÔNG BÁO THÀNH CÔNG VỀ CHO NGƯỜI DÙNG
        bot_reply_and_print(message, "Tải trang web hoàn tất")

    except Exception as e:
        print("Loading trang web thất bại")
        bot_reply_and_print(message, "Tải trang web thất bại")

    # XÓA CẤU HÌNH HIỆN TẠI
    try:
        bot_reply_and_print(message, "Xoá cấu hình hiện tại")

        # CLICK VÀO NÚT XOÁ CẤU HÌNH
        driver.find_element(By.XPATH, '//button[@class="btn btn-circle btn-dark btn-sm waves-effect waves-light btn-status-live" and @data-status="-1" and @data-toggle="tooltip"]').click()

        print("Click vào nút Xóa cấu hình")

        # ĐỢI THÔNG BÁO XOÁ CẤU HÌNH THÀNH CÔNG XUẤT HIỆN
        # KHI THÔNG BÁO XUẤT HIỆN THÌ => CẤU HÌNH ĐÃ ĐƯỢC XOÁ THÀNH CÔNG
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))
        bot_reply_and_print(message, "Xóa cấu hình thành công")

    except Exception as e:
        bot_reply_and_print(message, "Hiện tại không có cấu hình nào")

    # TẠO CẤU HÌNH MỚI
    bot_reply_and_print(message, "Tiến hành tạo cấu hình mới")

    # CHỌN TÀI KHOẢN
    print("Đang chọn tài khoản => nick-phu-lbh")
    driver.find_element(By.CSS_SELECTOR, "#tiktok_account > option:nth-child(4)").click() #Chọn tài khoản có tên nick-phu-lbh

    sleep(1) # CHỜ 1 GIÂY TRƯỚC KHI THỰC HIỆN TÁC VỤ TIẾP THEO

    # NHẬP TIÊU ĐỀ LIVE
    print("Đang nhập tiêu đề live => kéo rank Liên Quân")
    driver.find_element(By.ID, "title").send_keys("kéo rank Liên Quân")

    sleep(1) # CHỜ 1 GIÂY TRƯỚC KHI THỰC HIỆN TÁC VỤ TIẾP THEO

    # CHỌN CHỦ ĐỀ LIVE => GAMING
    print("Chọn chủ đề live => Gaming")
    driver.find_element(By.CSS_SELECTOR, "#topic > option:nth-child(11)").click() # Chọn chủ đề live Gaming

    sleep(1) # CHỜ 1 GIÂY TRƯỚC KHI THỰC HIỆN TÁC VỤ TIẾP THEO

    # CHỌN KIỂU LIVE => MOBILE
    print("Chọn kiểu live => Mobile")
    driver.find_element(By.CSS_SELECTOR, '#formLive > div:nth-child(6) > div > div > div > button:nth-child(2)').click()

    sleep(1) # CHỜ 1 GIÂY TRƯỚC KHI THỰC HIỆN TÁC VỤ TIẾP THEO

    # NHẬP LINK NGUỒN
    print("Nhập link nguồn")
    driver.find_element(By.ID, "url_source").send_keys(linknguon) # Nhập link nguồn

    sleep(1) # CHỜ 1 GIÂY TRƯỚC KHI THỰC HIỆN TÁC VỤ TIẾP THEO

    bot_reply_and_print(message, "Tạo cấu hình mới hoàn tất")
    
    sleep(1) # CHỜ 1 GIÂY TRƯỚC KHI THỰC HIỆN TÁC VỤ TIẾP THEO

    bot_reply_and_print(message, "Tiến hành lưu cấu hình...")

# LƯU CẤU HÌNH VÀ KIỂM TRA XEM CẤU HÌNH ĐÃ ĐƯỢC LƯU THÀNH CÔNG HAY CHƯA
    try:
        # CLICK VÀO NÚT LƯU CẤU HÌNH
        driver.find_element(By.CSS_SELECTOR, "#formLive > button").click()

        # CHO LOAD LẠI TRANG WEB
        driver.get('https://autolive.me/tiktok') #MỞ WEBSITE

        # KIỂM TRA XEM TRANG WEB LOAD XONG CHƯA
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[1]')))

        # SAU KHI TRANG WEB LOAD XONG THÌ => CẤU HÌNH ĐÃ ĐƯỢC LƯU LẠI
        print("TRANG WEB ĐÃ LOAD XONG => LƯU CẤU HÌNH THÀNH CÔNG")
        bot_reply_and_print(message, "Lưu cấu hình thành công")

    except Exception as e:
        print("LOAD TRANG WEB KHÔNG THÀNH CÔNG => LƯU CẤU HÌNH THẤT BẠI")
        bot_reply_and_print(message, "Lưu cấu hình mới thất bại")

    # MỞ LIVE
    try:
        bot_reply_and_print(message, "Tiến hành mở phiên live")
        print("Click vào nút MỞ LIVE")

        # CLICK VÀO NÚT MỞ LIVE
        driver.find_element(By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-status='1'][data-toggle='tooltip'][data-placement='top'][data-original-title='Bắt đầu live']").click()

        # ĐỢI THÔNG BÁO THÀNH CÔNG XUẤT HIỆN
        print("ĐỢI THÔNG BÁO MỞ LIVE THÀNH CÔNG XUẤT HIỆN")
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#table-live > tbody > tr > td:nth-child(10) > span')))
                                        
        print("THÔNG BÁO MỞ LIVE XUẤT HIỆN => MỞ LIVE THÀNH CÔNG")                                 
        bot_reply_and_print(message, "Mở live thành công")
    except:
        print("THÔNG BÁO MỞ LIVE KHÔNG XUẤT HIỆN => MỞ LIVE THẤT BẠI")
        bot_reply_and_print(message, "Mở live thất bại. KẾT THÚC TIẾN TRÌNH")
        driver.quit()

    # THÔNG BÁO CHO NGƯỜI DÙNG THỜI GIAN PHIÊN LIVE ĐƯỢC MỞ
    try:
        # MỞ PHIÊN LIVE
        driver.get('https://www.tiktok.com/@nammapsang_keorank/live')

        # KIỂM TRA XEM PHIÊN LIVE ĐÃ ĐƯỢC LOAD XONG CHƯA
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[1]/div/div[1]/a')))
        bot_reply_and_print(message, "Khi nào phiên live được diễn ra tôi sẽ thông báo cho bạn")
        
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
                    bot_reply_and_print(message, f"Phiên live đã được diễn ra vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")
                    driver.quit()
                    break

            except:
                print(f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live chưa được diễn ra => TIẾP TỤC KIỂM TRA...")
                driver.refresh()

    except Exception as e:
        bot_reply_and_print(message, "Kiểm tra thất bại")
        driver.quit()
################ KẾT THÚC LỆNH MỞ LIVE NICK PHỤ LBH ################

############# KIỂM TRA PHIÊN LIVE NICK PHỤ LBH SAU 1 TIẾNG #################
@bot.message_handler(commands=['checklive_nickphulbh'])
def checklive_nickphulbh(message):

    bot_reply_and_print(message, "Thực thi lệnh thành công, phiên live sẽ được kiểm tra sau 1 giờ nữa")

    countdown(60)
    # KHỞI TẠO WEBDRIVER
    driver = webdriver.Chrome(service=service, options=options)

    bot_reply_and_print(message, "1 tiếng đã trôi qua, tiến hành kiểm tra phiên live")
    bot_reply_and_print(message, "Truy cập vào phiên live")

    # KIỂM TRA XEM CÓ TRUY CẬP PHIÊN LIVE THÀNH CÔNG HAY KHÔNG
    try:
        driver.get('https://www.tiktok.com/@nammapsang_keorank/live')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[1]/div/div[1]/a')))
        bot_reply = "Truy cập phiên live thành công \nKhi phiên live dưới 5 người xem tôi sẽ tự động tắt live"
        bot_reply_and_print(message, f'{bot_reply}')
    except TimeoutException:
        bot_reply = "Truy cập live thất bại"
        bot_reply_and_print(message, "Kết thúc tiến trình")
        bot_reply_and_print(message, f'{bot_reply}')
        driver.quit()        

    # KIỂM TRA SỐ LƯỢNG NGƯỜI XEM CỦA PHIÊN LIVE SAU 1 TIẾNG
    while True:
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))
            now = datetime.datetime.now()
            
            checkview = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div")
            view = checkview.text

            if int(view) > 5:
                print(f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live hiện tại có {view} người xem => TIẾP TỤC KIỂM TRA...")
                driver.refresh()
            else:
                bot_reply_and_print(message, f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live hiện tại đang có {view} người xem => Tiến hành tắt live")
                driver.quit()
                tatlive(message)
                return
        except TimeoutException:
            bot_reply_and_print(message, "Không check được số người xem live, có vẻ như phiên live đã bị sập.")
            driver.quit()
            return
####################### KẾT THÚC MÃ KIỂM TRA PHIÊN LIVE NICK PHỤ LBH SAU 1 TIẾNG ###################

####################### BẮT ĐẦU MÃ CHỨC NĂNG TẮT LIVE #################################
@bot.message_handler(commands=['tatlive'])
def tatlive(message):

    # KHỞI TẠO WEBDRIVER
    driver = webdriver.Chrome(service=service, options=options)

    bot_reply_and_print(message, "Thực thi lệnh tắt live thành công")

    sleep(1)

    bot_reply_and_print(message, "Tiến hành truy cập vào web live")

#### MỞ WEB LIVE VÀ KIỂM TRA XEM PHIÊN LIVE ĐÃ ĐƯỢC MỞ THÀNH CÔNG HAY CHƯA ###

    # MỞ WEB LIVE
    driver.get('https://autolive.me/tiktok')

    # KIỂM TRA XEM WEBSITE ĐÃ LOAD XONG HAY CHƯA
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/h3/b')))
        bot_reply_and_print(message, "Truy cập vào web live thành công")
    except TimeoutException:
        bot_reply_and_print(message, "Truy cập vào web live thất bại, vui lòng kiểm tra lại kết nối internet và thử lại sau")
        driver.quit()
        return
    
    ################################ TẮT LIVE #################################

    bot_reply_and_print(message, "Tiến hành tắt live")

    try:
        # Kiểm tra giá trị data-original-title của button (Nếu là Dừng live thì mới click)
        button_tatlive = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-original-title='Dừng live']"))
    )
        if button_tatlive.get_attribute("data-original-title") == "Dừng live":
            button_tatlive.click() # CLICK VÀO NÚT TẮT LIVE NẾU GIÁ TRỊ HỢP LỆ                                     
    except:
        bot_reply_and_print(message, "Hiện tại không có phiên live nào được mở")
        driver.quit()
        return

    # KIỂM TRA SỰ KIỆN TẮT LIVE CÓ THÀNH CÔNG HAY KHÔNG
    try:
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div > div.notifyjs-container > div'))) # ĐỢI THÔNG BÁO TẮT LIVE THÀNH CÔNG XUẤT HIỆN
        bot_reply_and_print(message, "TẮT LIVE THÀNH CÔNG")
        driver.quit()
        return
    except TimeoutException:
        bot_reply_and_print(message, "TẮT LIVE KHÔNG THÀNH CÔNG, VUI LÒNG KIỂM TRA LẠI")
        driver.quit()
        return
####################### KẾT THÚC MÃ CHỨC NĂNG TẮT LIVE ###################

####################### BẮT ĐẦU MÃ MỞ LIVE VĂN BẢO #################################
@bot.message_handler(commands=['molive_vanbao'])
def molive_vanbao(message):

    driver = webdriver.Chrome(service=service, options=options) # Khởi tạo webdriver
    print("Khởi tạo WEBDRIVER")        

    bot_reply_and_print(message, "Thực thi lệnh thành công")
    sleep(1)
    
    bot_reply_and_print(message, "Mở web LIVE")
    sleep(1)

    bot_reply_and_print(message, "Đang tải trang web...")
    sleep(1)

    # MỞ TRANG WEB LIVE VÀ KIỂM TRA XEM TRANG WEB LOAD THÀNH CÔNG HAY CHƯA
    try:
        driver.get('https://autolive.me/tiktok') #MỞ WEB                      

        # KIỂM TRA XEM TRANG WEB ĐÃ LOAD XONG HAY CHƯA
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[1]')))
        
        # GỬI THÔNG BÁO THÀNH CÔNG VỀ CHO NGƯỜI DÙNG
        bot_reply_and_print(message, "Tải trang web hoàn tất")

    except Exception as e:
        print("Loading trang web thất bại")
        bot_reply_and_print(message, "Tải trang web thất bại")

    # XÓA CẤU HÌNH HIỆN TẠI
    try:
        bot_reply_and_print(message, "Xoá cấu hình hiện tại")

        # CLICK VÀO NÚT XOÁ CẤU HÌNH
        driver.find_element(By.XPATH, '//button[@class="btn btn-circle btn-dark btn-sm waves-effect waves-light btn-status-live" and @data-status="-1" and @data-toggle="tooltip"]').click()

        print("Click vào nút Xóa cấu hình")

        # ĐỢI THÔNG BÁO XOÁ CẤU HÌNH THÀNH CÔNG XUẤT HIỆN
        # KHI THÔNG BÁO XUẤT HIỆN THÌ => CẤU HÌNH ĐÃ ĐƯỢC XOÁ THÀNH CÔNG
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))
        bot_reply_and_print(message, "Xóa cấu hình thành công")

    except Exception as e:
        bot_reply_and_print(message, "Hiện tại không có cấu hình nào")

    # TẠO CẤU HÌNH MỚI
    bot_reply_and_print(message, "Tiến hành tạo cấu hình mới")

    # CHỌN TÀI KHOẢN
    print("Đang chọn tài khoản => van-bao")
    driver.find_element(By.CSS_SELECTOR, "#tiktok_account > option:nth-child(3)").click() #Chọn tài khoản có tên nick-phu-lbh

    sleep(1) # CHỜ 1 GIÂY TRƯỚC KHI THỰC HIỆN TÁC VỤ TIẾP THEO

    # NHẬP TIÊU ĐỀ LIVE
    print("Đang nhập tiêu đề live => kéo rank Liên Quân")
    driver.find_element(By.ID, "title").send_keys("kéo rank Liên Quân")

    sleep(1) # CHỜ 1 GIÂY TRƯỚC KHI THỰC HIỆN TÁC VỤ TIẾP THEO

    # CHỌN CHỦ ĐỀ LIVE => GAMING
    print("Chọn chủ đề live => Gaming")
    driver.find_element(By.CSS_SELECTOR, "#topic > option:nth-child(11)").click() # Chọn chủ đề live Gaming

    sleep(1) # CHỜ 1 GIÂY TRƯỚC KHI THỰC HIỆN TÁC VỤ TIẾP THEO

    # CHỌN KIỂU LIVE => MOBILE
    print("Chọn kiểu live => Mobile")
    driver.find_element(By.CSS_SELECTOR, '#formLive > div:nth-child(6) > div > div > div > button:nth-child(2)').click()

    sleep(1) # CHỜ 1 GIÂY TRƯỚC KHI THỰC HIỆN TÁC VỤ TIẾP THEO

    # NHẬP LINK NGUỒN
    print("Nhập link nguồn")
    driver.find_element(By.ID, "url_source").send_keys(linknguon) # Nhập link nguồn

    sleep(1) # CHỜ 1 GIÂY TRƯỚC KHI THỰC HIỆN TÁC VỤ TIẾP THEO

    bot_reply_and_print(message, "Tạo cấu hình mới hoàn tất")
    
    sleep(1) # CHỜ 1 GIÂY TRƯỚC KHI THỰC HIỆN TÁC VỤ TIẾP THEO

    bot_reply_and_print(message, "Tiến hành lưu cấu hình...")

# LƯU CẤU HÌNH VÀ KIỂM TRA XEM CẤU HÌNH ĐÃ ĐƯỢC LƯU THÀNH CÔNG HAY CHƯA
    try:
        # CLICK VÀO NÚT LƯU CẤU HÌNH
        driver.find_element(By.CSS_SELECTOR, "#formLive > button").click()

        # CHO LOAD LẠI TRANG WEB
        driver.get('https://autolive.me/tiktok') #MỞ WEBSITE

        # KIỂM TRA XEM TRANG WEB LOAD XONG CHƯA
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[1]')))

        # SAU KHI TRANG WEB LOAD XONG THÌ => CẤU HÌNH ĐÃ ĐƯỢC LƯU LẠI
        print("TRANG WEB ĐÃ LOAD XONG => LƯU CẤU HÌNH THÀNH CÔNG")
        bot_reply_and_print(message, "Lưu cấu hình thành công")

    except Exception as e:
        print("LOAD TRANG WEB KHÔNG THÀNH CÔNG => LƯU CẤU HÌNH THẤT BẠI")
        bot_reply_and_print(message, "Lưu cấu hình mới thất bại")

    # MỞ LIVE
    try:
        bot_reply_and_print(message, "Tiến hành mở phiên live")
        print("Click vào nút MỞ LIVE")

        # CLICK VÀO NÚT MỞ LIVE
        driver.find_element(By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-status='1'][data-toggle='tooltip'][data-placement='top'][data-original-title='Bắt đầu live']").click()

        # ĐỢI THÔNG BÁO THÀNH CÔNG XUẤT HIỆN
        print("ĐỢI THÔNG BÁO MỞ LIVE THÀNH CÔNG XUẤT HIỆN")
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#table-live > tbody > tr > td:nth-child(10) > span')))
                                        
        print("THÔNG BÁO MỞ LIVE XUẤT HIỆN => MỞ LIVE THÀNH CÔNG")                                 
        bot_reply_and_print(message, "Mở live thành công")
    except:
        print("THÔNG BÁO MỞ LIVE KHÔNG XUẤT HIỆN => MỞ LIVE THẤT BẠI")
        bot_reply_and_print(message, "Mở live thất bại. KẾT THÚC TIẾN TRÌNH")
        driver.quit()

    # THÔNG BÁO CHO NGƯỜI DÙNG THỜI GIAN PHIÊN LIVE ĐƯỢC MỞ
    try:
        # MỞ PHIÊN LIVE
        driver.get('https://www.tiktok.com/@vanbao165201/live')

        # KIỂM TRA XEM PHIÊN LIVE ĐÃ ĐƯỢC LOAD XONG CHƯA
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[1]/div/div[1]/a')))
        bot_reply_and_print(message, "Khi nào phiên live được diễn ra tôi sẽ thông báo cho bạn")
        
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
                    bot_reply_and_print(message, f"Phiên live đã được diễn ra vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")
                    driver.quit()
                    break

            except:
                print(f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live chưa được diễn ra => TIẾP TỤC KIỂM TRA...")
                driver.refresh()

    except Exception as e:
        bot_reply_and_print(message, "Kiểm tra thất bại")
        driver.quit()
################ KẾT THÚC LỆNH MỞ LIVE NICK CHÍNH VĂN BẢO ################

############# KIỂM TRA PHIÊN LIVE NICK CHÍNH VĂN BẢO SAU 1 TIẾNG #################
@bot.message_handler(commands=['checklive_vanbao'])
def checklive_vanbao(message):

    bot_reply_and_print(message, "Thực thi lệnh thành công, phiên live sẽ được kiểm tra sau 1 giờ nữa")
    countdown(60)    

    # KHỞI TẠO WEBDRIVER
    driver = webdriver.Chrome(service=service, options=options)

    bot_reply_and_print(message, "1 tiếng đã trôi qua, tiến hành kiểm tra phiên live")
    bot_reply_and_print(message, "Truy cập vào phiên live")

    # KIỂM TRA XEM CÓ TRUY CẬP PHIÊN LIVE THÀNH CÔNG HAY KHÔNG
    try:
        driver.get('https://www.tiktok.com/@vanbao165201/live')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[1]/div/div[1]/a')))
        bot_reply = "Truy cập phiên live thành công \nKhi phiên live dưới 5 người xem tôi sẽ tự động tắt live"
        bot_reply_and_print(message, f'{bot_reply}')
    except TimeoutException:
        bot_reply = "Truy cập live thất bại"
        bot_reply_and_print(message, "Kết thúc tiến trình")
        bot_reply_and_print(message, f'{bot_reply}')
        driver.quit()        

    # KIỂM TRA SỐ LƯỢNG NGƯỜI XEM CỦA PHIÊN LIVE SAU 1 TIẾNG
    while True:
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))
            now = datetime.datetime.now()
            
            checkview = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div")
            view = checkview.text

            if int(view) > 5:
                print(f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live hiện tại có {view} người xem => TIẾP TỤC KIỂM TRA...")
                driver.refresh()
            else:
                bot_reply_and_print(message, f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live hiện tại đang có {view} người xem => Tiến hành tắt live")
                driver.quit()
                tatlive(message)
                return
        except TimeoutException:
            bot_reply_and_print(message, "Không check được số người xem live, có vẻ như phiên live đã bị sập.")
            driver.quit()
            return
####################### KẾT THÚC MÃ KIỂM TRA PHIÊN LIVE NICK CHÍNH VĂN BẢO SAU 1 TIẾNG ###################    

################ CHỨC NĂNG MỞ LIVE NICK BÉ KHỂNH DÂU TÂY #######################
@bot.message_handler(commands=['molive_bekhenhdautay'])
def molive_bekhenhdautay(message):

    driver = webdriver.Chrome(service=service, options=options) # Khởi tạo webdriver
    print("Khởi tạo WEBDRIVER")        

    bot_reply_and_print(message, "Thực thi lệnh thành công")
    sleep(1)
    
    bot_reply_and_print(message, "Mở web LIVE")
    sleep(1)

    bot_reply_and_print(message, "Đang tải trang web...")
    sleep(1)

    # MỞ TRANG WEB LIVE VÀ KIỂM TRA XEM TRANG WEB LOAD THÀNH CÔNG HAY CHƯA
    try:
        driver.get('https://autolive.me/tiktok') #MỞ WEB                      

        # KIỂM TRA XEM TRANG WEB ĐÃ LOAD XONG HAY CHƯA
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[1]')))
        
        # GỬI THÔNG BÁO THÀNH CÔNG VỀ CHO NGƯỜI DÙNG
        bot_reply_and_print(message, "Tải trang web hoàn tất")

    except Exception as e:
        print("Loading trang web thất bại")
        bot_reply_and_print(message, "Tải trang web thất bại")

    # XÓA CẤU HÌNH HIỆN TẠI
    try:
        bot_reply_and_print(message, "Xoá cấu hình hiện tại")

        # CLICK VÀO NÚT XOÁ CẤU HÌNH
        driver.find_element(By.XPATH, '//button[@class="btn btn-circle btn-dark btn-sm waves-effect waves-light btn-status-live" and @data-status="-1" and @data-toggle="tooltip"]').click()

        print("Click vào nút Xóa cấu hình")

        # ĐỢI THÔNG BÁO XOÁ CẤU HÌNH THÀNH CÔNG XUẤT HIỆN
        # KHI THÔNG BÁO XUẤT HIỆN THÌ => CẤU HÌNH ĐÃ ĐƯỢC XOÁ THÀNH CÔNG
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.notifyjs-corner > div > div.notifyjs-container > div")))
        bot_reply_and_print(message, "Xóa cấu hình thành công")

    except Exception as e:
        bot_reply_and_print(message, "Hiện tại không có cấu hình nào")

    # TẠO CẤU HÌNH MỚI
    bot_reply_and_print(message, "Tiến hành tạo cấu hình mới")

    # CHỌN TÀI KHOẢN
    print("Đang chọn tài khoản => BÉ KHỂNH DÂU TÂY")
    driver.find_element(By.CSS_SELECTOR, "#tiktok_account > option:nth-child(2)").click() #Chọn tài khoản có tên nick-phu-lbh

    sleep(1) # CHỜ 1 GIÂY TRƯỚC KHI THỰC HIỆN TÁC VỤ TIẾP THEO

    # NHẬP TIÊU ĐỀ LIVE
    print("Đang nhập tiêu đề live => kéo rank Liên Quân")
    driver.find_element(By.ID, "title").send_keys("kéo rank Liên Quân")

    sleep(1) # CHỜ 1 GIÂY TRƯỚC KHI THỰC HIỆN TÁC VỤ TIẾP THEO

    # CHỌN CHỦ ĐỀ LIVE => GAMING
    print("Chọn chủ đề live => Gaming")
    driver.find_element(By.CSS_SELECTOR, "#topic > option:nth-child(11)").click() # Chọn chủ đề live Gaming

    sleep(1) # CHỜ 1 GIÂY TRƯỚC KHI THỰC HIỆN TÁC VỤ TIẾP THEO

    # CHỌN KIỂU LIVE => MOBILE
    print("Chọn kiểu live => Mobile")
    driver.find_element(By.CSS_SELECTOR, '#formLive > div:nth-child(6) > div > div > div > button:nth-child(2)').click()

    sleep(1) # CHỜ 1 GIÂY TRƯỚC KHI THỰC HIỆN TÁC VỤ TIẾP THEO

    # NHẬP LINK NGUỒN
    print("Nhập link nguồn")
    driver.find_element(By.ID, "url_source").send_keys(linknguon) # Nhập link nguồn

    sleep(1) # CHỜ 1 GIÂY TRƯỚC KHI THỰC HIỆN TÁC VỤ TIẾP THEO

    bot_reply_and_print(message, "Tạo cấu hình mới hoàn tất")
    
    sleep(1) # CHỜ 1 GIÂY TRƯỚC KHI THỰC HIỆN TÁC VỤ TIẾP THEO

    bot_reply_and_print(message, "Tiến hành lưu cấu hình...")

# LƯU CẤU HÌNH VÀ KIỂM TRA XEM CẤU HÌNH ĐÃ ĐƯỢC LƯU THÀNH CÔNG HAY CHƯA
    try:
        # CLICK VÀO NÚT LƯU CẤU HÌNH
        driver.find_element(By.CSS_SELECTOR, "#formLive > button").click()

        # CHO LOAD LẠI TRANG WEB
        driver.get('https://autolive.me/tiktok') #MỞ WEBSITE

        # KIỂM TRA XEM TRANG WEB LOAD XONG CHƯA
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div[1]/div/div[1]')))

        # SAU KHI TRANG WEB LOAD XONG THÌ => CẤU HÌNH ĐÃ ĐƯỢC LƯU LẠI
        print("TRANG WEB ĐÃ LOAD XONG => LƯU CẤU HÌNH THÀNH CÔNG")
        bot_reply_and_print(message, "Lưu cấu hình thành công")

    except Exception as e:
        print("LOAD TRANG WEB KHÔNG THÀNH CÔNG => LƯU CẤU HÌNH THẤT BẠI")
        bot_reply_and_print(message, "Lưu cấu hình mới thất bại")

    # MỞ LIVE
    try:
        bot_reply_and_print(message, "Tiến hành mở phiên live")
        print("Click vào nút MỞ LIVE")

        # CLICK VÀO NÚT MỞ LIVE
        driver.find_element(By.CSS_SELECTOR, "button.btn.btn-circle.btn-dark.btn-sm.waves-effect.waves-light.btn-status-live[data-status='1'][data-toggle='tooltip'][data-placement='top'][data-original-title='Bắt đầu live']").click()

        # ĐỢI THÔNG BÁO THÀNH CÔNG XUẤT HIỆN
        print("ĐỢI THÔNG BÁO MỞ LIVE THÀNH CÔNG XUẤT HIỆN")
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#table-live > tbody > tr > td:nth-child(10) > span')))
                                        
        print("THÔNG BÁO MỞ LIVE XUẤT HIỆN => MỞ LIVE THÀNH CÔNG")                                 
        bot_reply_and_print(message, "Mở live thành công")
    except:
        print("THÔNG BÁO MỞ LIVE KHÔNG XUẤT HIỆN => MỞ LIVE THẤT BẠI")
        bot_reply_and_print(message, "Mở live thất bại. KẾT THÚC TIẾN TRÌNH")
        driver.quit()

    # THÔNG BÁO CHO NGƯỜI DÙNG THỜI GIAN PHIÊN LIVE ĐƯỢC MỞ
    try:
        # MỞ PHIÊN LIVE
        driver.get('https://www.tiktok.com/@phuoc19903/live')

        # KIỂM TRA XEM PHIÊN LIVE ĐÃ ĐƯỢC LOAD XONG CHƯA
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[1]/div/div[1]/a')))
        bot_reply_and_print(message, "Khi nào phiên live được diễn ra tôi sẽ thông báo cho bạn")
        
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
                    bot_reply_and_print(message, f"Phiên live đã được diễn ra vào lúc {now.strftime('%d/%m/%Y %H:%M:%S')}")
                    driver.quit()
                    break

            except:
                print(f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live chưa được diễn ra => TIẾP TỤC KIỂM TRA...")
                driver.refresh()

    except Exception as e:
        bot_reply_and_print(message, "Kiểm tra thất bại")
        driver.quit()
################ KẾT THÚC LỆNH MỞ LIVE NICK BÉ KHỂNH DÂU TÂY ################

############# KIỂM TRA PHIÊN LIVE NICK BÉ KHỂNH DÂU TÂY SAU 1 TIẾNG #################
@bot.message_handler(commands=['checklive_bekhenhdautay'])
def checklive_bekhenhdautay(message):
    bot_reply_and_print(message, "Thực thi lệnh thành công, phiên live sẽ được kiểm tra sau 1 giờ nữa")
    countdown(60)

    # KHỞI TẠO WEBDRIVER
    driver = webdriver.Chrome(service=service, options=options)

    bot_reply_and_print(message, "1 tiếng đã trôi qua, tiến hành kiểm tra phiên live")
    bot_reply_and_print(message, "Truy cập vào phiên live")

    # KIỂM TRA XEM CÓ TRUY CẬP PHIÊN LIVE THÀNH CÔNG HAY KHÔNG
    try:
        driver.get('https://www.tiktok.com/@phuoc19903/live')
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[1]/div/div[1]/a')))
        bot_reply = "Truy cập phiên live thành công \nKhi phiên live dưới 5 người xem tôi sẽ tự động tắt live"
        bot_reply_and_print(message, f'{bot_reply}')
    except TimeoutException:
        bot_reply = "Truy cập live thất bại"
        bot_reply_and_print(message, "Kết thúc tiến trình")
        bot_reply_and_print(message, f'{bot_reply}')
        driver.quit()        

    # KIỂM TRA SỐ LƯỢNG NGƯỜI XEM CỦA PHIÊN LIVE SAU 1 TIẾNG
    while True:
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div')))
            now = datetime.datetime.now()
            
            checkview = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div/div")
            view = checkview.text

            if int(view) > 5:
                print(f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live hiện tại có {view} người xem => TIẾP TỤC KIỂM TRA...")
                driver.refresh()
            else:
                bot_reply_and_print(message, f"{now.strftime('%d/%m/%Y %H:%M:%S')} - Phiên live hiện tại đang có {view} người xem => Tiến hành tắt live")
                driver.quit()
                tatlive(message)
                return
        except TimeoutException:
            bot_reply_and_print(message, "Không check được số người xem live, có vẻ như phiên live đã bị sập. Vui lòng kiểm tra lại tài khoản")
            driver.quit()
            return
        
################################################################################################################        

#################################### CHỨC NĂNG KHỞI ĐỘNG LẠI BOT ###############################################

################################################################################################################

@bot.message_handler(commands=['restart'])
def handle_restart(message):
    restart_bot(message)

# Hàm để restart bot
def restart_bot(message):
    driver = webdriver.Chrome(service=service, options=options)
    bot_reply_and_print(message, "Khởi động lại bot thành công")
    driver.quit()  # Đóng trình duyệt Selenium trước khi restart
    os.execv(sys.executable, ['python'] + sys.argv)
 ################################## KẾT THÚC CHỨC NĂNG KHỞI ĐỘNG LẠI BOT #####################################

########################################################
####################### CHẠY BOT #######################
########################################################
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception("LỖI")
        time.sleep(5)