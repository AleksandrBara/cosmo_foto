import telegram
import os
from time import sleep
import random
from dotenv import load_dotenv
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("pause")
    launch_number = parser.parse_args().pause
    return launch_number


def send_fotos_bot(pause, chat_id):


    for address, dirs, files in os.walk('space_images'):
        file_path_catalog = list()
        for name in files:
            file_path = os.path.join(address, name)
            file_path_catalog.append(file_path)
            bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))
            sleep(1)
    while True:
        random.shuffle(file_path_catalog)
        for file_path in file_path_catalog:
            bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))
            sleep(14)

if __name__ == '__main__':
    load_dotenv()
    chat_id = os.getenv("chat_id")
    Token = os.getenv("TOKEN_TELEGRAM")
    bot = telegram.Bot(token=Token)



#     raise NetworkError(f'urllib3 HTTPError {error}') from error
# telegram.error.NetworkError: urllib3
# HTTPError('Connection aborted.', timeout('The write operation timed out'))