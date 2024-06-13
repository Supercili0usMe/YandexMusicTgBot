from yandex_music import Client

client = Client("y0_AgAAAABKXGhzAAG8XgAAAADQNjJ3efAwYTLuSlmTKBcHy7zXcl0OthM").init()
search_list = client.search("The Little Things Give You Away")
track = search_list.best
track.result.download("example.mp3", bitrate_in_kbps=320)
track = track.to_dict()
print(track.keys())