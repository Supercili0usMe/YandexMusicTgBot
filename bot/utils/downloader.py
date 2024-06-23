from yandex_music import Client

def search_list(token, query, page):
    client = Client(token)
    search = client.search(text=query, page=page).tracks
    track_list = []
    for elem in search.results:
        tot_sec = elem.duration_ms // 1000
        temp = f"{', '.join(elem.artists_name())} - {elem.title} [{tot_sec//60}:{tot_sec%60:02d}]"
        track_list.append(temp)
    return track_list, search.total, search

def download_track(tracks, id):
    client = Client().init()
    track = tracks.results[id]
    track.download(f'{track.title}.mp3', bitrate_in_kbps=320)
    
if __name__ == "__main__":
    token = "y0_AgAAAABKXGhzAAG8XgAAAADQNjJ3efAwYTLuSlmTKBcHy7zXcl0OthM"
    page = 0
    input_query = input('Введите поисковой запрос: ')
    while True:
        track_list, total, tracks = return_search_list(token, input_query, page)
        print(f'\nВот что мне удалось найти в интернете по запросу "{input_query}"')
        print(f'Общее число найденных треков: {total}, страница: {page}')
        for i, r in enumerate(track_list):
            print(f"{i}: {r}")
        ans = str(input('Введите номер трека или далее: '))
        if ans.isalpha():
            page += 1
        elif ans.isdigit():
            download_track(tracks, int(ans))
            break