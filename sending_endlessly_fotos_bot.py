import telegram
import os
import random
from dotenv import load_dotenv
import argparse
from time import sleep
from secondary_function import get_file_paths_from_directory
from secondary_function import send_picture_to_telegram


def get_time_out_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--time_out", default=14400)
    time_out = parser.parse_args().time_out
    return time_out


def send_pictures_to_telegram_endlessly(token, chat_id, file_paths):
    for file_path in file_paths:
        try:
            send_picture_to_telegram(token, chat_id, file_path)
            sleep(int(time_out))
        except (telegram.error.Unauthorized, telegram.error.InvalidToken) as e:
            quit('Проверьте ваши данные! \n Ошибка:\n{}'.format(e))
        except telegram.error.NetworkError as e:
            print('Отсутствует подключение! \n Ошибка:\n{}'.format(e))
            sleep(600)
    while True:
        random.shuffle(file_paths)
        for file_path in file_paths:
            try:
                send_picture_to_telegram(token, chat_id, file_path)
                sleep(int(time_out))
            except (telegram.error.Unauthorized, telegram.error.InvalidToken) as e:
                quit('Проверьте ваши данные! \n Ошибка:\n{}'.format(e))
            except telegram.error.NetworkError as e:
                print('Отсутствует подключение! \n Ошибка:\n{}'.format(e))
                sleep(600)


if __name__ == '__main__':
    load_dotenv()
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    token = os.getenv("TELEGRAM_TOKEN")
    time_out = get_time_out_from_args()
    directory = 'space_images'
    file_paths = get_file_paths_from_directory(directory)
    send_pictures_to_telegram_endlessly(token, chat_id, file_paths)
