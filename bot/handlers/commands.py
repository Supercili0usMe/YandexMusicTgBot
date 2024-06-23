from telebot import types
import sqlite3
from bot.handlers.callback import *

def commands_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Перейди на сайт!", url="https://youtu.be/dQw4w9WgXcQ")
        markup.row(btn1)
        btn2 = types.InlineKeyboardButton("Удалить фото", callback_data="delete")
        btn3 = types.InlineKeyboardButton("Хочу мем", callback_data="edit")
        markup.row(btn2, btn3)
        with open("bot/data/hqdefault.jpg", 'rb') as file:
            bot.send_photo(message.chat.id, file, reply_markup=markup)
        bot.register_next_step_handler(message, lambda msg: on_click(bot, msg))

    @bot.message_handler(commands=["weather"])
    def weather(message):
        bot.send_message(message.chat.id, 'Спорим ты напишешь название города, а я выведу текущую погоду в нём')
        bot.register_next_step_handler(message, lambda msg: get_weather(bot, msg))

    @bot.message_handler(commands=["database"])
    def start(message):
        conn = sqlite3.connect("bot/data/temp.sql")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, pass TEXT)")
        conn.commit()
        cursor.close()
        conn.close()

        bot.send_message(message.chat.id, "Привет, а я тебя в табличку щас запишу, поэтому введи свое имя:")
        bot.register_next_step_handler(message, lambda msg: user_name(bot, msg))

    @bot.message_handler(commands=["help"])
    def answer(message):
        bot.send_message(message.chat.id, "||Полезная|| информация", parse_mode='MarkdownV2')

    @bot.message_handler(commands=["info"])
    def answer(message):
        bot.send_message(message.chat.id, message)
