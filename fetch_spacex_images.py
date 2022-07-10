import requests
import urllib.parse
import os
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--launch_number", default=55)
    launch_number = parser.parse_args().launch_number
    return launch_number


def make_file_name_from_link(link):
    url_component = urllib.parse.urlparse(link).path
    url_component_clean = urllib.parse.unquote(url_component)
    file_name = os.path.split(url_component_clean)[1]
    return file_name


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
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)
    launch_number = get_args()
    try:
        links = fetch_spacex_any_launch(launch_number)
        for link in links:
            file_name = make_file_name_from_link(link)
            file_path = f'{directory_name}/{file_name}'
            response = requests.get(link)
            response.raise_for_status()
            with open(file_path, 'wb') as file:
                file.write(response.content)
    except (
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError
    ) as e:
        print('Не возможно получить данные с сервера:\n{}'.format(e))
