import os


def create_folder_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        return
    for file_name in os.listdir(folder_name):
        file_path = f'{folder_name}/{file_name}'
        if os.path.isfile(file_path):
            os.remove(file_path)


def create_file_if_not_exists(folder_name, file_name):
    file_path = f'{folder_name}/{file_name}'
    file = open(file_path, 'w+')
    file.close()
