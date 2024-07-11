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

# KHAI BÁO APT TOKEN BOT TELEGRAM
API_TOKEN = '7329003333:AAF7GhjivbGnk0jSGE8XfefFh_-shHAFsGc'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

chat_id = '5634845912' # ID CỦA NGƯỜI DÙNG

# HÀM ĐẾM NGƯỢC SỐ PHÚT
def countdown(minutes):
    total_seconds = minutes * 60
    for i in range(total_seconds, 0, -1):
        minutes, seconds = divmod(i, 60)
        print(f"Còn {minutes} phút {seconds} giây nữa sẽ tiến hành kiểm tra phiên live.")
        time.sleep(1)
    print("Đếm ngược hoàn tất, tiến hành kiểm tra trạng thái phiên live")

# HÀM IN VĂN BẢN THÀNH MÀU ĐỎ
def print_red(text):
    red_color_code = "\033[91m"
    reset_code = "\033[0m"
    print(f"{red_color_code}[*] {text}{reset_code}")

# IN VĂN BẢN THÀNH MÀU ĐỎ VÀ GỬI TIN NHẮN VỀ CHO NGƯỜI DÙNG
def print_red_and_send_message(text, chat_id):
    red_color_code = "\033[91m"
    reset_code = "\033[0m"
    formatted_text = f"{red_color_code}[*] {text}{reset_code}"
    
    # In văn bản màu đỏ
    print(formatted_text)
    
    # Gửi tin nhắn tới người dùng
    bot.send_message(chat_id, f"[*] {text}")    

# HÀM IN VĂN BẢN THÀNH MÀU VÀNG
def print_yellow(text):
    yellow_color_code = "\033[93m"
    reset_code = "\033[0m"
    print(f"{yellow_color_code}[*] {text}{reset_code}")

# IN VĂN BẢN THÀNH MÀU VÀNG VÀ GỬI TIN NHẮN VỀ CHO NGƯỜI DÙNG
def print_yellow_and_send_message(text, chat_id):
    yellow_color_code = "\033[93m"
    reset_code = "\033[0m"
    formatted_text = f"{yellow_color_code}[*] {text}{reset_code}"
    
    # In văn bản màu vàng
    print(formatted_text)
    
    # Gửi tin nhắn tới người dùng
    bot.send_message(chat_id, f"[*] {text}")    

# HÀM IN VĂN BẢN THÀNH MÀU XANH LÁ CÂY
def print_green(text):
    green_color_code = "\033[92m"
    reset_code = "\033[0m"
    print(f"{green_color_code}[*] {text}{reset_code}")

# IN VĂN BẢN THÀNH MÀU XANH LÁ CÂY VÀ GỬI TIN NHẮN VỀ CHO NGƯỜI DÙNG
def print_green_and_send_message(text, chat_id):
    green_color_code = "\033[92m"
    reset_code = "\033[0m"
    formatted_text = f"{green_color_code}[*] {text}{reset_code}"
    
    # In văn bản màu xanh lá cây
    print(formatted_text)
    
    # Gửi tin nhắn tới người dùng
    bot.send_message(chat_id, f"[*] {text}")