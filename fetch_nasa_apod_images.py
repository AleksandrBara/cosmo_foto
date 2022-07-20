import requests
import os
import argparse
from dotenv import load_dotenv
from pathlib import Path
from secondary_function import make_time_stamp
from secondary_function import make_file_extension_from_link
from secondary_function import save_link_as_picture


def get_counter_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", default=5)
    count = parser.parse_args().count
    return count


def fetch_nasa_apod_images(token, foto_count):
    headers = {}
    payload = ('api_key', token), ('count', foto_count)
    response = requests.get(
        'https://api.nasa.gov/planetary/apod',
        headers=headers,
        params=payload
    )
    response.raise_for_status()
    foto_discriptions = response.json()
    for foto_discription in foto_discriptions:
        link = foto_discription['hdurl']
        file_extension = make_file_extension_from_link(link)
        file_name = f"'NASA'{make_time_stamp()}{file_extension}"
        file_path = Path(directory_name, file_name)
        save_link_as_picture(link, file_path)


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv("NASA_TOKEN")
    directory_name = 'space_images'
    os.makedirs(directory_name, exist_ok=True)
    foto_count = get_counter_from_args()
    try:
        links = fetch_nasa_apod_images(token, foto_count)
    except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError
    ) as e:
        print('Не возможно получить данные с сервера:\n{}'.format(e))
