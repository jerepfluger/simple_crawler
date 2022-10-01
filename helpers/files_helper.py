import os


def create_folder_if_not_exists(folder_name, bot_name):
    directory = f'{folder_name}/{bot_name}'
    if not os.path.exists(directory):
        os.makedirs(directory)
        return
    for file_name in os.listdir(directory):
        file_path = f'{directory}/{file_name}'
        if os.path.isfile(file_path):
            os.remove(file_path)
