from pytube import YouTube, Playlist


# ask uesr of input data
def ask_user_of_input_data():
    playlist = Playlist(input("Podaj link do playlisty (pamiętaj że nie może być niepubliczna: "))
    playlist = list(playlist.__reversed__())

    print("Twoją playlistę zapiszemy w katalogu E:\YouTube\WatchLater. \n"
          "Jeśli chcesz by była umieszczona w podkatalogu podaj go poniżej. W innym przpypadku po prostu naciśnij Enter")
    path = f"E:\YouTube\WatchLater\{input('Do jakiego podfolderu zapisać plik: ')}"
    print(f"Zapiszemy plalistę w katalogu: {path} \n")

    x = input("Od jakiego numeru zacząć numerować: ")
    start_counting_number = int(x) if x else 1
    print(f"Zaczniemy numerować od: {start_counting_number} \n")

    return playlist, path, start_counting_number


def check_highest_avaliable_resolution(yt_video):
    if 'itag="22"' in str(yt_video.streams.filter(progressive=True)):
        itag = 22  # sprawdzam czy video posaida itag=22 (rozdzielczość 720p)
    elif 'itag="18"' in str(yt_video.streams.filter(progressive=True)):
        itag = 18  # sprawdzam czy video posaida itag=18 (rozdzielczość 360p)
    else:  # jeśli nie ma video dostępnego ani w 720p ani 360p to informuje o tym
        print(f'nie udało się pobrać video: {yt_video.title} (brak dostępnej jakości)')
        itag = 0
    return itag


def download_playlist(playlist, start_counting_number, path):
    list_of_failure = []
    print(f"Pobieram {len(playlist)} filmów \n")
    for index, video_url in enumerate(playlist):
        yt_video = YouTube(video_url)  # create YT object from next url from playlist

        valid_file_name = prepare_valid_file_information(index, yt_video, start_counting_number)

        itag = check_highest_avaliable_resolution(yt_video)
        if not itag:
            list_of_failure.append(valid_file_name)

        xd = download_video(yt_video, itag, index, valid_file_name, path)
        if xd:
            list_of_failure.append(xd)

    return list_of_failure


def download_video(yt_video, itag, index, valid_file_name, path):
    try:
        yt_video.streams.get_by_itag(itag).download(filename=valid_file_name, output_path=path)
        resolution = '720p' if itag == 22 else '360p'
        print(f'pobieram video numer {index} w jakości {resolution}: {yt_video.title}')
    except:
        print(f'nie udało pobrać się {yt_video.title} (błąd pobierania)')
        return yt_video.title


def prepare_valid_file_information(index, yt_video, start_counting_number):
    # prepare
    video_counter = ("00" + str(index + start_counting_number))[-3:]  # format 0012 <- slice last 3 position
    video_title = yt_video.title
    video_author = yt_video.author
    file_name = f'{video_counter} {video_title} [{video_author}].mp4'

    # valid
    not_valid_char = r"""\/*:?"<>|"""  # check in Windows
    valid_file_name = ''.join(['' if char in not_valid_char else char for char in file_name])

    # result
    return valid_file_name


def summary(list_of_failure, playlist):
    print(f'\n\n Pobieranie ukończone! '
          f'\n ilość video które udało się pobrać: {len(playlist) - len(list_of_failure)}/{len(playlist)}'
          f'\n video których nie udało się pobrać: {len(list_of_failure)} \n')
    for failure in list_of_failure:
        print(failure)
