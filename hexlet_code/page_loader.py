import string
from pathlib import Path

import requests


def get_filename_for_url(url: str) -> str:
    _, url_without_scheme = url.split('://', maxsplit=1)
    filename = ''
    for s in url_without_scheme:
        if s not in string.ascii_letters + string.digits:
            filename += '-'
        else:
            filename += s

    return f'{filename}.html'


def download(url: str, directory: str) -> str:
    response = requests.get(url)
    filename = get_filename_for_url(url)
    filepath = Path(directory) / filename
    # filepath.write_text(response.text)
    with open(filepath, 'w') as f:
        f.write(response.text)
    return str(filepath)
