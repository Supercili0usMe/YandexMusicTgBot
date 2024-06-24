import telebot
from telebot import types
from bot.config import TELEGRAM_BOT_TOKEN

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Словарь для хранения состояний пользователей
user_states = {}

# Определение состояний
class BotStates:
    START = "start"
    WAITING_FOR_SONG = "waiting_for_song"

@bot.message_handler(commands=['start'])
def start(message):
    send_welcome_message(message.chat.id)
    user_states[message.from_user.id] = BotStates.START

def send_welcome_message(chat_id):
    markup = types.InlineKeyboardMarkup()
    hello_message = "👋 Добро пожаловать! \n\n Я пока что тестовая версия поэтому жмякай на кнопочки"
    btn1 = types.InlineKeyboardButton("Скачать песенку", callback_data="first_function")
    markup.row(btn1)
    bot.send_message(chat_id, hello_message, reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    user_id = callback.from_user.id
    if callback.data == 'first_function':
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("<< Вернуться в начало", callback_data="back")
        markup.add(btn)
        bot.edit_message_text("Введи название песни или исполнителя, а я тебе отправлю результат поиска", 
                              callback.message.chat.id, 
                              callback.message.message_id, 
                              reply_markup=markup)
        user_states[user_id] = BotStates.WAITING_FOR_SONG
    elif callback.data == 'back':
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        send_welcome_message(callback.message.chat.id)
        user_states[user_id] = BotStates.START

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == BotStates.WAITING_FOR_SONG)
def handle_song_name(message):
    song_name = message.text
    bot.send_message(message.chat.id, f"Вы ввели: {song_name}")

# Отладочный модуль
if __name__ == "__main__":
    print('Запуск бота...')
    bot.infinity_polling()
