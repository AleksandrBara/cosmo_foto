import telegram
import os
import random
from dotenv import load_dotenv
import argparse
from time import sleep


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--time_out", default=14400)
    time_out = parser.parse_args().time_out
    return time_out


def get_file_paths_from_directory(directory):
    all_file_paths = list()
    for address, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(address, name)
            all_file_paths.append(file_path)
    return all_file_paths


if __name__ == '__main__':
    load_dotenv()
    chat_id = os.getenv("SPACE_CHAT_ID")
    token = os.getenv("TELEGRAM_TOKEN")
    time_out = get_args()
    directory = 'space_images'
    file_paths = get_file_paths_from_directory(directory)
    bot = telegram.Bot(token=token)
    try:
        for file_path in file_paths:
            with open(file_path, 'rb') as file:
                bot.send_document(chat_id=chat_id, document=file)
            sleep(int(time_out))
    except (telegram.error.NetworkError, telegram.error.InvalidToken) as e:
        print('Ошибка:\n{}'.format(e))
    while True:
        random.shuffle(file_paths)
        try:
            for file_path in file_paths:
                with open(file_path, 'rb') as file:
                    bot.send_document(chat_id=chat_id, document=file)
                sleep(int(time_out))
        except (telegram.error.NetworkError, telegram.error.InvalidToken) as e:
            print('Ошибка:\n{}'.format(e))
