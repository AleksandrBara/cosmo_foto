import requests
from pathlib import Path
import os
from secondary_function import save_link_as_picture


def get_links_and_all_id_from_nasa():
    url = "https://epic.gsfc.nasa.gov/api/natural"
    payload = {}
    headers = {}
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    fotos_descriptions = response.json()
    links_and_all_id = list()
    for fotos_description in fotos_descriptions:
        image_id = str(fotos_description['image'])
        day_id = str(fotos_description['date'])
        day_id, _ = day_id.replace('-', '/').split(' ')
        link = f'https://epic.gsfc.nasa.gov/archive/natural/{day_id}/png/{image_id}.png'
        link_and_id = (link, image_id)
        links_and_all_id.append(link_and_id)
    return links_and_all_id


def save_links_as_pictures(links_and_all_id):
    for link, image_id in links_and_all_id:
        file_name = f"{image_id}.png"
        file_path = Path(directory_name, file_name)
        save_link_as_picture(link, file_path)


if __name__ == '__main__':
    directory_name = 'space_images'
    os.makedirs(directory_name, exist_ok=True)
    try:
        links_and_all_id = get_links_and_all_id_from_nasa()
        save_links_as_pictures(links_and_all_id)
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print('Не возможно получить данные с сервера:\n{}'.format(e))
