import os
from configparser import ConfigParser

config = ConfigParser()
config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_file_path)

# Проверки на конфигурацию:
if 'telegram' not in config:
    raise KeyError("Секция 'telegram' не найдена в config.ini")
if 'TELEGRAM_BOT_TOKEN' not in config["telegram"]:
    raise KeyError("Ключ 'TELEGRAM_BOT_TOKEN' не найден в секции 'telegram' в config.ini")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or config["telegram"]["TELEGRAM_BOT_TOKEN"]

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("Токен бота не найден ни в переменных окружения, ни в файле конфигурации")

if __name__ == "__main__":
    print(TELEGRAM_BOT_TOKEN)