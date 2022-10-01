import os


def create_folder_if_not_exists(bot_name):
    if not os.path.exists(bot_name):
        os.makedirs(bot_name)
        return
    for file in os.listdir(bot_name):
        if os.path.isfile(file):
            os.remove(file)
            continue
