import pytest
import io
from unittest.mock import patch
from werkzeug.datastructures import Headers
from freezeyt.freezer import Freezer

INPUT_DATA = [
    (
        (io.BytesIO(b"<a href='/second_page.html'>LINK</a>"),
        "http://localhost:8000/",
        [('Content-Type', 'text/html; charset=utf-8')]),
        ['/second_page.html']
    )

]


@pytest.mark.parametrize("values, expected", INPUT_DATA)
def test_get_links_by_content_type(monkeypatch, values, expected):
    file, url, headers = values

    monkeypatch.setattr(
        'freezeyt.filesaver.FileSaver.open_filename', lambda _: file)

    result = Freezer.get_links_by_type(Freezer, file, url, Headers(headers))

    assert result == expected
