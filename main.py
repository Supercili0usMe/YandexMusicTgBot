from telebot import TeleBot
from configparser import ConfigParser

# Чтение из конфигурационного файла
config = ConfigParser()
config.read("config.ini")
bot = TeleBot(config['telegram']["TELEGRAM_BOT_TOKEN"])

# Обработка стартовых команд 
@bot.message_handler(commands=["start", 'main', 'hello'])
def answer(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.username}!")

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


# Отладочный модуль
if __name__ == "__main__":
    print('Запуск бота...')
    bot.infinity_polling()