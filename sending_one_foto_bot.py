import telegram
import os
import random
from dotenv import load_dotenv
import argparse
from secondary_function import get_file_paths_from_directory
from secondary_function import send_picture_to_telegram


def get_file_path_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", default=None)
    file_path = parser.parse_args().file_path
    return file_path


if __name__ == '__main__':
    load_dotenv()
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    token = os.getenv("TELEGRAM_TOKEN")
    directory = 'space_images'
    file_path = get_file_path_from_args()
    if file_path is None:
        file_path_catalog = get_file_paths_from_directory(directory)
        file_path = random.choice(file_path_catalog)
    try:
        send_picture_to_telegram(token, chat_id, file_path)
    except (telegram.error.NetworkError, telegram.error.Unauthorized) as e:
        print('Ошибка:\n{}'.format(e))
