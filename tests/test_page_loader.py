import sys

import pytest

from hexlet_code.page_loader import download, get_filename_for_url


@pytest.fixture
def expected_file_path():
    return 'file_fixtures/expected.html'


def get_file_fixture_content(filename: str) -> str:
    with open(f'tests/file_fixtures/{filename}') as f:
        return f.read()


def test_download_simple_success(tmp_path, requests_mock):
    url = 'https://example.com/simple'
    expected_file_name = 'example-com-simple.html'
    expected_content = get_file_fixture_content('expected.html')
    requests_mock.get(url, text=expected_content)

    file_path = download(url, str(tmp_path))

    assert file_path == str(tmp_path / expected_file_name)
    with open(file_path) as f:
        assert f.read() == expected_content


@pytest.mark.parametrize(
    ('url', 'filename'),
    (
        ('https://example.com/simple.html', 'example-com-simple-html.html'),
        ('https://sub-domain.example.com/a_b(1)#23-__--5', 'sub-domain-example-com-a-b-1--23-----5.html'),
    )
)
def test_get_filename_for_url(url, filename):
    assert get_filename_for_url(url) == filename
