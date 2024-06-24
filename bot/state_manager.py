class BotStates:
    START = "start"
    WAITING_FOR_SONG = "waiting_for_song"
    SEARCHING_TRACK = "searching_track"

# Глобальный словарь для хранения состояний пользователей
user_states = {}

def set_state(user_id, state):
    user_states[user_id] = state

def get_state(user_id):
    return user_states.get(user_id, BotStates.START)