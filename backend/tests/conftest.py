import pytest
import json

@pytest.fixture
def mock_css_colors():
    with open('css_colors.json', 'r') as file:
        return json.load(file)["colors"]