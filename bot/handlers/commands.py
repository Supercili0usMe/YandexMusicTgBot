from telebot import types
from bot.state_manager import BotStates, set_state

def commands_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        send_welcome_message(bot, message.chat.id)
        set_state(message.from_user.id, BotStates.START)

def send_welcome_message(bot, chat_id):
    markup = types.InlineKeyboardMarkup()
    hello_message = "👋 Добро пожаловать! \n\n Я пока что тестовая версия поэтому жмякай на кнопочки"
    btn1 = types.InlineKeyboardButton("Скачать песенку", callback_data="download_music")
    markup.row(btn1)
    bot.send_message(chat_id, hello_message, reply_markup=markup)

