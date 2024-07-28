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
from dylib import dylib

# KHAI BÁO APT TOKEN BOT TELEGRAM
API_TOKEN = '7371036517:AAEB8PtQRtSrvDOxQUUW2su7ObGso6ltq8w'  # TOKEN CỦA BOT
bot = telebot.TeleBot(API_TOKEN)

chat_id = '5634845912' # ID CỦA NGƯỜI DÙNG

# IMPORT CHỨC NĂNG MỞ LIVE

# MỞ LIVE TÀI KHOẢN MEME LỎ
from molive.molive_memelo import main_molive_memelo

# MỞ LIVE TÀI KHOẢN VĂN BẢO
from molive.molive_vanbao import main_molive_vanbao

# MỞ LIVE TÀI KHOẢN NICK PHU LBH
from molive.molive_nickphulbh import main_molive_nickphulbh

# IMPORT CHỨC NĂNG CHECKLIVE

# CHECKLIVE MEME LỎ
from checklive.checklive_memelo import main_checklive_memelo

# CHECK LIVE VĂN BẢO
from checklive.checklive_vanbao import main_checklive_vanbao

# CHECK LIVE NICK PHU LBH
from checklive.checklive_nickphulbh import main_checklive_nickphulbh

# IMPORT CHỨC NĂNG TẮT LIVE
from tatlive.tatlive import main_tatlive

########################### BẮT ĐẦU CÁC CHỨC NĂNG CỦA BOT ###########################
print(f"============= | KHỞI ĐỘNG BOT LIVESTREAM THÀNH CÔNG | =============")

########################## BẮT ĐẦU CÁC CHỨC NĂNG MỞ LIVE ###############################

# CHỨC NĂNG MỞ LIVE TÀI KHOẢN MEME LỎ
@bot.message_handler(commands=['molive_memelo'])
def molive_memelo(message):
    main_molive_memelo(message)

# CHỨC NĂNG MỞ LIVE TÀI KHOẢN NICK-PHU-LBH
@bot.message_handler(commands=['molive_nickphulbh'])
def molive_nickphulbh(message):
    main_molive_nickphulbh(message)

# CHỨC NĂNG MỞ LIVE TÀI KHOẢN VĂN BẢO
@bot.message_handler(commands=['molive_vanbao'])
def molive_vanbao(message):
    main_molive_vanbao(message)

########################## BẮT ĐẦU CÁC CHỨC NĂNG CHECK LIVE ###############################        

# CHỨC NĂNG CHECK LIVE MEME LỎ
@bot.message_handler(commands=['checklive_memelo'])
def checklive_meme_lo(message):
    main_checklive_memelo(message)
    dylib.countdown(60)
    main_tatlive(message)

# CHỨC NĂNG CHECK LIVE VĂN BẢO
@bot.message_handler(commands=['checklive_vanbao'])
def checklive_vanbao(message):
    main_checklive_vanbao(message)
    dylib.countdown(60)
    main_tatlive(message)

# CHỨC NĂNG CHECK LIVE NICK PHU LBH
@bot.message_handler(commands=['checklive_nickphulbh'])
def checklive_nickphulbh(message):
    main_checklive_nickphulbh(message)
    dylib.countdown(60)
    main_tatlive(message)    


############################## CHỨC NĂNG TẮT LIVE #######################################
@bot.message_handler(commands=['tatlive'])
def tatlive(message):
    main_tatlive(message)    

########################  TEST CHỨC NĂNG MỚI ####################
from thunghiem.test import main_test
@bot.message_handler(commands=['test'])
def test(message):
    dylib.countdown(60)

############################## CHỨC NĂNG LIVE TỰ ĐỘNG #######################################
@bot.message_handler(commands=['autolive'])
def auto_live(message):
    # MỞ LIVE TÀI KHOẢN MEME LỎ
    molive_memelo(message)

    # CHECK LIVE MEME LỎ
    checklive_meme_lo(message)

    # MỞ LIVE TÀI KHOẢN NICK PHU LBH
    molive_nickphulbh(message)

    # CHECK LIVE NICK PHU LBH
    checklive_vanbao(message)

########################################################
####################### CHẠY BOT #######################
########################################################
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception("LỖI")
        time.sleep(5)