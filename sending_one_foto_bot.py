import telegram
import os
import random
from dotenv import load_dotenv
import argparse
from secondary_function import get_file_paths_from_directory


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", default=None)
    file_path = parser.parse_args().file_path
    return file_path


if __name__ == '__main__':
    directory = 'space_images'
    load_dotenv()
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
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
