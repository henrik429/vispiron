import pytest
import json
from backend.app.models import CSSColor


@pytest.fixture
def mock_css_colors():
    with open('css_colors.json', 'r') as file:
        colors_data = json.load(file)["colors"]
        filtered_colors = [
            CSSColor(name=color.get("name"), hex=color.get("hex"), rgb=color.get("rgb"))
            for color in colors_data
        ]
        return filtered_colors