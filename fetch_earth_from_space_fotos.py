import urllib.parse
import requests
import urllib.parse
import os


def make_file_name_from_link(link):
    url_component = urllib.parse.urlparse(link).path
    url_component_clean = urllib.parse.unquote(url_component)
    file_name = os.path.split(url_component_clean)[1]
    return file_name


def fetch_earth_from_space_fotos():
    url = "https://epic.gsfc.nasa.gov/api/natural"
    payload = {}
    headers = {}
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    fotos_descriptions = response.json()
    links = list()
    for fotos_description in fotos_descriptions:
        image_id = str(fotos_description['image'])
        day_id = str(fotos_description['date'])
        day_id, _ = day_id.replace('-', '/').split(' ')
        link = f'https://epic.gsfc.nasa.gov/archive/natural/{day_id}/png/{image_id}.png'
        links.append(link)
    return links


if __name__ == '__main__':
    directory_name = 'space_images'
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)
    try:
        links = fetch_earth_from_space_fotos()
        for link in links:
            file_name = make_file_name_from_link(link)
            file_path = f'{directory_name}/{file_name}'
            response = requests.get(link)
            response.raise_for_status()
            with open(file_path, 'wb') as file:
                file.write(response.content)
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print('Не возможно получить данные с сервера:\n{}'.format(e))