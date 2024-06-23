from telebot import TeleBot
from bot.config import TELEGRAM_BOT_TOKEN
import bot.handlers as handlers

# Инициализация бота
bot = TeleBot(TELEGRAM_BOT_TOKEN)

# Регистрация обработчиков
handlers.commands_handlers(bot)
handlers.callback_handlers(bot)
handlers.messages_handlers(bot)


# Отладочный модуль
if __name__ == "__main__":
    print('Запуск бота...')
    bot.infinity_polling()