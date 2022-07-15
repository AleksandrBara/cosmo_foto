import telegram
import os
import random
from dotenv import load_dotenv
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", default=None)
    file_path = parser.parse_args().file_path
    return file_path


def get_file_paths_from_directory(directory):
    for address, dirs, files in os.walk(directory):
        all_file_paths= list()
        for name in files:
            file_path = os.path.join(address, name)
            all_file_paths.append(file_path)
    return all_file_paths


if __name__ == '__main__':
    directory = 'space_images'
    load_dotenv()
    chat_id = os.getenv("SPACE_CHAT_ID")
    token = os.getenv("TELEGRAM_TOKEN")
    file_path = get_args()
    if file_path is None:
        file_path_catalog = get_file_paths_from_directory(directory)
        file_path = random.choice(file_path_catalog)
    bot = telegram.Bot(token=token)
    try:
        with open(file_path, 'rb') as file:
            bot.send_document(chat_id=chat_id, document=file)
    except (telegram.error.NetworkError, telegram.error.InvalidToken) as e:
        print('Ошибка:\n{}'.format(e))
