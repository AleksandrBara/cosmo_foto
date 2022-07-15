import requests
import urllib.parse
import os
import argparse
from dotenv import load_dotenv
import datetime
from pathlib import Path


def make_time_stamp():
    current_time = datetime.datetime.now()
    time_stamp = current_time.strftime("%Y%m%d%H%M%S")
    return time_stamp


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", default=5)
    count = parser.parse_args().count
    return count


def make_file_extension_from_link(link):
    url_component = urllib.parse.urlparse(link).path
    url_component_clean = urllib.parse.unquote(url_component)
    file_extension = os.path.splitext(url_component_clean)[1]
    return file_extension


def get_astronomy_picture_of_the_day(token, foto_count):
    directory_name = 'space_images'
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)
    headers = {}
    payload = ('api_key', token), ('count', foto_count)
    response = requests.get(
        'https://api.nasa.gov/planetary/apod',
        headers=headers,
        params=payload
    )
    response.raise_for_status()
    foto_discriptions = response.json()
    links = list()
    for foto_discription in foto_discriptions:
        link = foto_discription['hdurl']
        links.append(link)
    return links


if __name__ == '__main__':
    directory_name = 'space_images'
    os.makedirs(directory_name, exist_ok=True)
    load_dotenv()
    token = os.getenv("NASA_TOKEN")
    foto_count = get_args()
    try:
        links = get_astronomy_picture_of_the_day(token, foto_count)
    except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError
    ) as e:
        quit('Не возможно получить данные с сервера:\n{}'.format(e))
    for link in links:
        file_extension = make_file_extension_from_link(link)
        file_name = f"'NASA'{make_time_stamp()}{file_extension}"
        file_path = Path(directory_name, file_name)
        try:
            response = requests.get(link)
            response.raise_for_status()
        except (
                requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError
        ) as e:
            print('Не возможно получить данные с сервера:\n{}'.format(e))
        with open(file_path, 'wb') as file:
            file.write(response.content)
