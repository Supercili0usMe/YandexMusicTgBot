from telebot import TeleBot
from telebot import types
from bot.config import TELEGRAM_BOT_TOKEN

# Чтение из конфигурационного файла
bot = TeleBot(TELEGRAM_BOT_TOKEN)

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

# Обработка стартовых команд 
@bot.message_handler(commands=["start", 'main', 'hello'])
def answer(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Перейди на сайт!", url="https://youtu.be/dQw4w9WgXcQ")
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton("Удалить фото", callback_data="delete")
    btn3 = types.InlineKeyboardButton("Изменить текст", callback_data="edit")
    markup.row(btn2, btn3)
    bot.reply_to(message, f"Привет, {message.from_user.username}!", reply_markup=markup)

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