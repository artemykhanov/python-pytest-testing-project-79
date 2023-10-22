import sys

import pytest

from hexlet_code.page_loader import download


@pytest.fixture
def expected_file_path():
    return 'file_fixtures/expected.html'


def test_download(tmp_path, expected_file_path):
    url = ''
    directory = tmp_path / 'test_directory'
    print(directory)
    file_path = download(url, str(directory))
    with open(file_path) as f, open(expected_file_path) as expected_file:
        assert f.read() == expected_file.read()

