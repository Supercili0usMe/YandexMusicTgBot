from telebot import TeleBot
from telebot import types
from bot.config import TELEGRAM_BOT_TOKEN
import sqlite3

# Чтение из конфигурационного файла
bot = TeleBot(TELEGRAM_BOT_TOKEN)
name = None

#Обработка стартовой функции
@bot.message_handler(commands=["start"])
def start(message):
    # Создаем БД
    conn = sqlite3.connect("temp.sql")
    cursor = conn.cursor()

    # Создаём таблицу
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))")
    conn.commit()
    cursor.close()
    conn.close()

    bot.send_message(message.chat.id, "Привет, а я тебя в табличку щас запишу, поэтому введи свое имя:")
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "Введите пароль:")
    bot.register_next_step_handler(message, user_pwd)

def user_pwd(message):
    pwd = message.text.strip()

    conn = sqlite3.connect("temp.sql")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, pwd))
    conn.commit()
    cursor.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, "Харош", reply_markup=markup)

@bot.callback_query_handler(func= lambda call:True)
def callback(call):
    conn = sqlite3.connect("temp.sql")
    cursor = conn.cursor()
    cursor.execute("SELECT * from users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    info = ''
    for el in users:
        info += f"Имя: {el[1]}, Пароль: {el[2]}\n"
    
    bot.send_message(call.message.chat.id, info)


# Обработка файлов
@bot.message_handler(content_types=["photo"])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Перейди на сайт!", url="https://youtu.be/dQw4w9WgXcQ")
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton("Удалить фото", callback_data="delete")
    btn3 = types.InlineKeyboardButton("Изменить текст", callback_data="edit")
    markup.row(btn2, btn3)
    bot.reply_to(message, "Красивое...", reply_markup=markup)

# Обработка внутренних функций
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text("Edit text", callback.message.chat.id, callback.message.message_id)

# Обработка стартовых команд 
@bot.message_handler(commands=['main', 'hello'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("Перейди на сайт!")
    markup.row(btn1)
    btn2 = types.KeyboardButton("Удалить фото")
    btn3 = types.KeyboardButton("Хочу мем")
    markup.row(btn2, btn3)
    with open(".\YandexMusicTgBot\hqdefault.jpg", 'rb') as file:
        bot.send_photo(message.chat.id, file, reply_markup=markup)
    # bot.send_message(message.chat.id, f"Привет, {message.from_user.username}!", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == "Перейди на сайт!":
        bot.send_message(message.chat.id, "ага, конечно")
    elif message.text == "Удалить фото":
        bot.send_message(message.chat.id, "Еще чего")
    elif message.text == "Хочу мем":
        bot.send_message(message.chat.id, "Перехочешь")

# Обработка команды help
@bot.message_handler(commands=["help"])
def answer(message):
    bot.send_message(message.chat.id, "||Полезная|| информация", parse_mode='MarkdownV2')

# Обработка команды info
@bot.message_handler(commands=["info"])
def answer(message):
    bot.send_message(message.chat.id, message)    

#Обработка любого текста, введённого пользователем
@bot.message_handler()
def info(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, f"Привет, {message.from_user.username}!")
    elif message.text.lower() == "id":
        bot.reply_to(message, f"ID: {message.from_user.id}")
    elif message.text.lower() == "я":
        bot.reply_to(message, "свинья))")


# Отладочный модуль
if __name__ == "__main__":
    print('Запуск бота...')
    bot.infinity_polling()