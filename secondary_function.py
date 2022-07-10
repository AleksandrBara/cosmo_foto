import urllib.parse
import os


def make_file_name_from_link(link):
    url_component = urllib.parse.urlparse(link).path
    url_component_clean = urllib.parse.unquote(url_component)
    file_name = os.path.split(url_component_clean)[1]
    return file_name


def get_file_paths_from_directory(directory):
    for address, dirs, files in os.walk(directory):
        file_path_catalog = list()
        for name in files:
            file_path = os.path.join(address, name)
            file_path_catalog.append(file_path)
    return file_path_catalog