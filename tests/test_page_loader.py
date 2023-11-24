import os.path

import pytest
import requests_mock

from hexlet_code.page_loader import download, make_path_by_url


def get_file_fixture_bytes(filename: str) -> bytes:
    with open(f'tests/file_fixtures/{filename}', 'rb') as f:
        return f.read()


def get_file_fixture_text(filename: str) -> str:
    with open(f'tests/file_fixtures/{filename}') as f:
        return f.read()


def test_download_simple_success(tmp_path, requests_mock):
    url = 'https://example.com/simple'
    expected_file_name = 'example-com-simple.html'
    expected_text = get_file_fixture_text('simple.html')
    requests_mock.get(url, text=expected_text)

    file_path = download(url, str(tmp_path))

    assert file_path == str(tmp_path / expected_file_name)
    with open(file_path) as f:
        assert f.read() == expected_text


@pytest.mark.parametrize(
    ('url', 'path'),
    (
        ('https://example.com/simple.html', 'example-com-simple-html'),
        ('https://sub-domain.example.com/a_b(1)#23-__--5', 'sub-domain-example-com-a-b-1--23-----5'),
        ('https://ru.hexlet.io/assets/professions/python', 'ru-hexlet-io-assets-professions-python'),
    )
)
def test_make_path_by_url(url, path):
    assert make_path_by_url(url) == path


def test_download_html_with_files(tmp_path):
    url = 'https://ru.hexlet.io/courses'
    file_url = 'https://ru.hexlet.io/assets/professions/python.png'
    another_domain_file_url = 'https://cdn2.hexlet.io/assets/error-pages/404-83b6e8d08445469eb3b4347ac5cfb08d98f3d7ba9a8e4134bf7070b227a42a2a.svg'  # E501

    with requests_mock.Mocker() as req_mock:
        req_mock.get(url, text=get_file_fixture_text('html-with-files.html'))
        req_mock.get(file_url, content=get_file_fixture_bytes('python.png'))
        req_mock.get(another_domain_file_url, content=get_file_fixture_bytes('404-error.svg'))

        file_path = download(url, str(tmp_path))

    expected_downloaded_html = get_file_fixture_text('html-with-files-downloaded.html')

    with open(file_path) as f:
        content = f.read()
        assert content == expected_downloaded_html

    filepath = str(tmp_path / 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-python.png')
    filepath_2 = str(tmp_path / 'ru-hexlet-io-courses_files/cdn2-hexlet-io-assets-error-pages-404-83b6e8d08445469eb3b4347ac5cfb08d98f3d7ba9a8e4134bf7070b227a42a2a.svg')

    assert os.path.exists(filepath)
    assert os.path.exists(filepath_2)
