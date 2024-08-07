import telebot
from telebot import types

API_TOKEN = '7371036517:AAEB8PtQRtSrvDOxQUUW2su7ObGso6ltq8w'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('hi')
    btn2 = types.KeyboardButton('hello')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Chào mừng! Hãy chọn một trong các nút dưới đây:", reply_markup=markup)

def hello(message):
    bot.send_message(message.chat.id, "Bạn đã chọn 'hi'!")

@bot.message_handler(func=lambda message: message.text in ["hi", "hello"])
def handle_message(message):
    if message.text == "hi":
        hello(message)
    elif message.text == "hello":
        bot.send_message(message.chat.id, "Bạn đã chọn 'hello'!")

bot.polling()
