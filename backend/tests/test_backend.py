from fastapi.testclient import TestClient
from backend.app.main import app
import pytest
from unittest.mock import patch
from backend.app.services import ColorService

import sys
print(sys.path)

client = TestClient(app)

def test_start_page():
    response = client.get("/colors")
    assert response.status_code == 200
    assert isinstance(response.json(), list)



@pytest.mark.parametrize(
    "color_list, expected_status, expected_color",
    [
        ([], 400, None),
        (["#AABBCC", "#154331", "#A0B1C2", "#000000", "#FFFFFF"], 200, "The brightest color is:  #FFFFFF (r=255, g=255, b=255), called White"),
        (["#123456"], 200, "The brightest color is:  #123456 (r=18, g=52, b=86), called MidnightBlue"),
        (["#000000", "#00FF00"], 200, "The brightest color is:  #00FF00 (r=0, g=255, b=0), called Lime"),
        (["#FFAA00", "#FFFF00", "#FF0000"], 200, "The brightest color is:  #FFFF00 (r=255, g=255, b=0), called Yellow"),
        (["#222222", "#888888", "#FFFFFF"], 200, "The brightest color is:  #FFFFFF (r=255, g=255, b=255), called White"),
    ]
)
@patch.object(ColorService, 'fetch_css_colors')
def test_get_brightest_color(mock_fetch_colors, mock_css_colors,  color_list, expected_status, expected_color):
    mock_fetch_colors.return_value = mock_css_colors

    color_service = ColorService(color_list)
    result = color_service.get_brightest_color_info()

    assert result == expected_color