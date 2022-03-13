from pytube import YouTube, Playlist

# dane_od_użytkownika:
playlist = Playlist(input("Podaj link do playlisty (pamiętaj że nie może być niepubliczna: "))
path = f"E:\YouTube\WatchLater\{input('Do jakiego podfolderu zapisać plik: ')}"
print(path)
x = input("Od jakiego numeru zacząć numerować: ")
beginning_video_count = int(x) if x else 0

# inne_dane:
zakazane_symbole = ['|', ':', '?', '"', "'", '&', '(', ')', '#', '/', '*']
list_of_failure = []

# Główna część programu
print(f'Zaczynam pobieranie {len(playlist)} filmów')


for index, video in enumerate(playlist):
    if index < 4:
        continue
    """
    x = 0 # jak coś pójdzie nie tak, to tu wpisujesz ostatinie udane pobieranie
    if index < x:  
        continue
    """
    # Tworzę zmienną, która będzie odświeżać link do filmu co obieg pętli
    yt_video = YouTube(video)

    # Tworzę informacje potrzebne do zapisania nazwy pliku
    video_count = str(("00" + str(index + beginning_video_count)))[-3:]
    video_title = yt_video.title
    video_author = yt_video.author
    video_name = f'{video_count} {video_title} [{video_author}].mp4'

    # Sprawdzam czy nazwa jest legitna
    for char in zakazane_symbole:
        if char in video_name:
            video_name = video_name.replace(char, '')

    # Sprawdzam dostępne jakości
    if 'itag="22"' in str(yt_video.streams.filter(progressive=True)):
        itag = 22  # sprawdzam czy video posaida itag=22 (rozdzielczość 720p)
    elif 'itag="18"' in str(yt_video.streams.filter(progressive=True)):
        itag = 18  # sprawdzam czy video posaida itag=18 (rozdzielczość 360p)
    else:  # jeśli nie ma video dostępnego ani w 720p ani 360p to informuje o tym
        print(f'nie udało się pobrać video: {video_name} (brak dostępnej jakości)')
        list_of_failure.append(video_name)
        itag = 0
        continue
    video_quality = '720p' if itag == 22 else '360p'

    # No i w końcu pobieranie
    try:
        print(f'pobieram video numer {index+1} w jakości {video_quality}: {video_name}')
        yt_video.streams.get_by_itag(itag).download(filename=video_name, output_path=path)
    except ValueError:
        print(f'nie udało pobrać się {video_name} (błąd pobierania)')
        list_of_failure.append(yt_video.title)

# Zakończenie i podsumowanie
print('\n\n Pobieranie ukończone! '
      f'\n ilość video które udało się pobrać: {len(playlist) - len(list_of_failure)}/{len(playlist)}'
      '\n\n video których nie udało się pobrać:', len(list_of_failure))
for failure in list_of_failure:
    print(failure)
