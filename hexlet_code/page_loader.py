import os.path
import string
from pathlib import Path
from urllib import parse

import requests
from bs4 import BeautifulSoup

# todo: использовать дата классы


def make_path_by_url(url: str) -> str:
    if "://" in url:
        _, url = url.split('://', maxsplit=1)
    path = ''
    for s in url:
        if s not in string.ascii_letters + string.digits:
            path += '-'
        else:
            path += s

    return path


def handle_files_in_html(html_text: str, files_directory: str, domain_with_scheme: str) -> tuple[list[dict], str]:
    soup = BeautifulSoup(html_text, 'html.parser')
    result = []
    for img in soup.find_all('img'):
        original_image_url_as_path = ensure_absolute_url(img['src'], domain_with_scheme)
        without_ext, ext = original_image_url_as_path.rsplit('.', maxsplit=1)
        # suffix = original_image_url_as_path.suffix
        downloaded_image_path = str(Path(files_directory) / f'{make_path_by_url(without_ext)}.{ext}')

        result.append({
            'original_url': img['src'],
            'downloaded_path': downloaded_image_path,
        })

        img['src'] = downloaded_image_path

    return result, soup.prettify()


def ensure_absolute_url(url: str, domain_with_scheme: str) -> str:
    parsed_url = parse.urlparse(url)
    if not parsed_url.netloc:
        url = f'{domain_with_scheme}{url}'
    return url


def download(url: str, directory: str) -> str:
    """

    Получить содержимое страницы по указанному URL
    Получить ссылки на ресурсы (картинки) из содержимого страницы и заменить их внутри страницы на путь к локальному файлу
    Скачать ресурсы в указанную директорию
    Сохранить страницу в указанную директорию
    """
    parsed_url = parse.urlparse(url)
    domain_with_scheme = f'{parsed_url.scheme}://{parsed_url.netloc}'
    response = requests.get(url)
    page_text = response.text

    path = make_path_by_url(url)
    files_directory = f'{path}_files'

    files, handled_page_text = handle_files_in_html(page_text, files_directory, domain_with_scheme)

    if files and not os.path.exists(Path(directory) / files_directory):
        os.mkdir(Path(directory) / files_directory)

    for file in files:
        file_url = ensure_absolute_url(file['original_url'], domain_with_scheme)
        file_path = Path(directory) / file['downloaded_path']
        response = requests.get(file_url)

        with open(file_path, 'wb') as f:
            f.write(response.content)

    filename = f'{path}.html'
    filepath = Path(directory) / filename

    with open(filepath, 'w') as f:
        f.write(handled_page_text)
    return str(filepath)
