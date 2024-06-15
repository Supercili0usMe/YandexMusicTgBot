from telebot import types
import sqlite3

def user_name(bot, message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "Введите пароль:")
    bot.register_next_step_handler(message, lambda msg: user_pwd(bot, msg))

def user_pwd(bot, message):
    pwd = message.text.strip()
    conn = sqlite3.connect("bot/data/temp.sql")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, pass) VALUES (?, ?)", (name, pwd))
    conn.commit()
    cursor.close()
    conn.close()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список пользователей', callback_data='callback'))
    bot.send_message(message.chat.id, "Харош", reply_markup=markup)

def on_click(bot, message):
    if message.text == "Перейди на сайт!":
        bot.send_message(message.chat.id, "ага, конечно")
    elif message.text == "Удалить фото":
        bot.send_message(message.chat.id, "Еще чего")
    elif message.text == "Хочу мем":
        bot.send_message(message.chat.id, "Перехочешь")

def callback_message(bot, callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text("Edit text", callback.message.chat.id, callback.message.message_id)

def callback(bot, call):
    conn = sqlite3.connect("bot/data/temp.sql")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    info = ''
    for el in users:
        info += f"Имя: {el[1]}, Пароль: {el[2]}\n"

    bot.send_message(call.message.chat.id, info)

def get_weather(bot, message):
    city = message.text.strip().lower()
    bot.send_message(message.chat.id, city)

def callback_handlers(bot):
    bot.register_callback_query_handler(lambda callback: callback_message(bot, callback), func=lambda callback: True)
    bot.register_callback_query_handler(lambda call: callback(bot, call), func=lambda call: True)

# Экспорт функций для использования в других модулях
__all__ = ['user_name', 'user_pwd', 'on_click', 'get_weather', 'callback_handlers']
