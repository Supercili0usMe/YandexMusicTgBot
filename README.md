## Yandex Music Bot Downloader

Structure:
* Directory `data`:
    * hqdefault.jpg - just random picture, i hope it wont be here forever
    * temp.sql - sqlite3-file, that contains all users, who use a bot (temporary)
* Directory `handlers`:
    * callback.py - handlers for postback requests (inline-menu button)
    * messages.py - handlers for text messages
    * commands.py - handlers for commands (for example `/start`, `/help` etc.)
* Directory `utils`:
    * downloader.py - function for search and download music from Yandex.Music
* `config.py` - file to load configurations from config.ini and provide them to other parts of the application
* `main.py` - the main bot launch file, in which all handlers are configured and launched
