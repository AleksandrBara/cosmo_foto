import requests
import urllib.parse
import os
import argparse
import datetime
from pathlib import Path


def make_time_stamp():
    current_time = datetime.datetime.now()
    time_stamp = current_time.strftime("%Y%m%d%H%M%S")
    return time_stamp


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch_number", default=55)
    launch_number = parser.parse_args().launch_number
    return launch_number


def make_file_extension_from_link(link):
    url_component = urllib.parse.urlparse(link).path
    url_component_clean = urllib.parse.unquote(url_component)
    file_extension = os.path.splitext(url_component_clean)[1]
    return file_extension


def fetch_spacex_any_launch(launch_number):
    url = "https://api.spacexdata.com/v3/launches/{}".format(launch_number)
    payload = {'filter': 'links'}
    headers = {}
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    links = response.json()['links']['flickr_images']
    return links


if __name__ == '__main__':
    directory_name = 'space_images'
    os.makedirs(directory_name, exist_ok=True)
    launch_number = get_args()
    try:
        links = fetch_spacex_any_launch(launch_number)
    except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError
    ) as e:
        print('Не возможно получить данные с сервера:\n{}'.format(e))

    for link in links:
        file_extension = make_file_extension_from_link(link)
        file_name = f"'spacex'{make_time_stamp()}{file_extension}"
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
