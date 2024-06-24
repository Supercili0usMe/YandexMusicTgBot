from telebot import types
from bot.state_manager import BotStates, set_state, get_state
from bot.handlers.commands import send_welcome_message
from bot.utils import *

# Глобальные переменные для страницы и названия песни
page = 0
song_name = ''
tracks = None

# Обработка текста от пользователя
def callback_handlers(bot):
    @bot.callback_query_handler(func=lambda callback: True)
    def handle_callback(callback):
        user_id = callback.from_user.id

        if callback.data == 'download_music':
            handle_download_music(bot, callback)
        elif callback.data == 'back':
            handle_back(bot, callback)
        elif callback.data in ["prev_page", "next_page"]:
            handle_pagination(bot, callback)
        elif callback.data.startswith("choose_track_"):
            handle_track_choice(bot, callback)

    @bot.message_handler(func=lambda message: get_state(message.from_user.id) == BotStates.WAITING_FOR_SONG)
    def handle_song_name_input(message):
        handle_song_search(bot, message)

def handle_download_music(bot, callback):
    user_id = callback.from_user.id
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("<< Вернуться в начало", callback_data="back")
    markup.add(btn)
    bot.edit_message_text(
        "Введи название песни или исполнителя, а я тебе отправлю результат поиска",
        callback.message.chat.id, 
        callback.message.message_id, 
        reply_markup=markup
    )
    set_state(user_id, BotStates.WAITING_FOR_SONG)

def handle_back(bot, callback):
    user_id = callback.from_user.id
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    if get_state(user_id) == "searching_track":
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 2)
    send_welcome_message(bot, callback.message.chat.id)
    set_state(user_id, BotStates.START)

def handle_pagination(bot, callback):
    global page
    global song_name
    if callback.data == "prev_page":
        page = max(0, page - 1)
    elif callback.data == "next_page":
        page += 1
    txt, markup = find_song(callback.message, song_name, page)
    bot.edit_message_text(
        txt, 
        callback.message.chat.id, 
        callback.message.message_id,
        reply_markup=markup,
        parse_mode="MarkdownV2"
    )

def handle_track_choice(bot, callback):
    track_id = int(callback.data.split("choose_track_")[1])
    send_track_info(bot, callback.message.chat.id, track_id)

def handle_song_search(bot, message):
    global page
    global song_name
    set_state(message.from_user.id, BotStates.SEARCHING_TRACK)
    page, song_name = 0, message.text
    txt, markup = find_song(message, song_name, page)
    bot.send_message(message.chat.id, txt, reply_markup=markup, parse_mode="MarkdownV2")

def find_song(message, song_name, page):
    global tracks
    key = "y0_AgAAAABKXGhzAAG8XgAAAADQNjJ3efAwYTLuSlmTKBcHy7zXcl0OthM"
    track_list, total, tracks = search_list(key, song_name, page)
    txt, markup = create_song_message(track_list, total, song_name, page)
    return txt, markup

def create_song_message(track_list: list, total: int, song_name: str, page: int):
    markup = types.InlineKeyboardMarkup()
    txt = (
        f'Вот что мне удалось найти в интернете по запросу: *{song_name}* \n\n'
        f'Общее число найденных треков: *{total}*, страница: *{page}*'
    )
    for id, elem in enumerate(track_list):
        btn = types.InlineKeyboardButton(f"{elem}", callback_data=f"choose_track_{id}")
        markup.row(btn)
    btn1 = types.InlineKeyboardButton("<", callback_data="prev_page")
    btn2 = types.InlineKeyboardButton("назад", callback_data="back")
    btn3 = types.InlineKeyboardButton(">", callback_data="next_page")
    markup.row(btn1, btn2, btn3)
    return txt, markup

def send_track_info(bot, chat_id: int, track_id: int):
    global tracks
    audio_file, title = download_track(tracks, track_id)
    bot.send_audio(chat_id, audio_file, title=title)
