import urllib.parse
import os
import datetime

def make_time_stamp():
    current_time = datetime.datetime.now()
    time_stamp = current_time.strftime("%Y%m%d%H%M%S")
    return time_stamp


def make_file_extension_from_link(link):
    url_component = urllib.parse.urlparse(link).path
    url_component_clean = urllib.parse.unquote(url_component)
    file_extension = os.path.splitext(url_component_clean)[1]
    return file_extension


def get_file_paths_from_directory(directory):
    for address, dirs, files in os.walk(directory):
        file_path_catalog = list()
        for name in files:
            file_path = os.path.join(address, name)
            file_path_catalog.append(file_path)
    return file_path_catalog