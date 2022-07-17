import requests
import os
import argparse
from pathlib import Path
from secondary_function import make_time_stamp
from secondary_function import make_file_extension_from_link


def get_lounch_number_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch_number", default=55)
    launch_number = parser.parse_args().launch_number
    return launch_number


def fetch_spacex_any_launch(launch_number):
    url = "https://api.spacexdata.com/v3/launches/{}".format(launch_number)
    payload = {'filter': 'links'}
    headers = {}
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    links = response.json()['links']['flickr_images']
    for link in links:
        file_extension = make_file_extension_from_link(link)
        file_name = f"'spacex'{make_time_stamp()}{file_extension}"
        file_path = Path(directory_name, file_name)
        response = requests.get(link)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            file.write(response.content)


if __name__ == '__main__':
    directory_name = 'space_images'
    os.makedirs(directory_name, exist_ok=True)
    launch_number = get_lounch_number_from_args()
    try:
        links = fetch_spacex_any_launch(launch_number)
    except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError
    ) as e:
        print('Не возможно получить данные с сервера:\n{}'.format(e))
