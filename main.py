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

# Обработка внутренних функций
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text("Edit text", callback.message.chat.id, callback.message.message_id)

# Обработка стартовых команд 
@bot.message_handler(commands=["start", 'main', 'hello'])
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