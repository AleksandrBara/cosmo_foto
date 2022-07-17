import telegram
import os
import random
from dotenv import load_dotenv
import argparse
from time import sleep
from secondary_function import get_file_paths_from_directory


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--time_out", default=14400)
    time_out = parser.parse_args().time_out
    return time_out



if __name__ == '__main__':
    load_dotenv()
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
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
