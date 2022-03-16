from YT_downloader_module import *

playlist, path, start_counting_number = ask_user_of_input_data()
list_of_failure = download_playlist(playlist, start_counting_number, path)
summary(list_of_failure, playlist)
