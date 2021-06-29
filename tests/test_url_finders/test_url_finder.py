import pytest
import io
from unittest.mock import patch
from werkzeug.datastructures import Headers
from freezeyt.freezer import Freezer
from freezeyt.getlinks_html import get_all_links
from freezeyt.getlinks_css import get_links_from_css

INPUT_DATA = [
    (
        (b"<a href='/second_page.html'>LINK</a>",
        "http://localhost:8000/",
        [('Content-Type', 'text/html; charset=utf-8')],
        "text/hmtl"),
        ['/second_page.html']
    )

]


@pytest.mark.parametrize("values, expected", INPUT_DATA)
def test_get_links_by_content_type(monkeypatch, values, expected):
    file, url, headers, config_type = values
    monkeypatch.setattr(Freezer, 'saver.open_filename', file)

    from unittest.mock import patch, mock_open
    with patch("builtins.open", mock_open(read_data="data")) as mock_file:
        assert open("path/to/open").read() == "data"
        mock_file.assert_called_with("path/to/open")

        result = Freezer.get_links_by_type(Freezer, file, url, Headers(headers))

        assert result == expected
