import numpy as np
from typing import List
from backend.app.config import CSS_COLORS_API_BASE_URL
from backend.app.models import CSSColor
import requests


class Color:
    def __init__(self, hex_value: str):
        self.hex_value = hex_value
        self.r, self.g, self.b = self.hex_to_rgb(hex_value)
        self.brightness = self.calc_brightness(r=self.r, g=self.g, b=self.b)

    @staticmethod
    def hex_to_rgb(hex_value: str):
        hex_value = hex_value.lstrip("#")
        return int(hex_value[0:2], 16), int(hex_value[2:4], 16), int(hex_value[4:6], 16)

    @staticmethod
    def calc_brightness(r: int, g: int, b: int) -> float:
        return np.sqrt(0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2))


class ColorService:
    def __init__(self, color_list: List[str]):
        self.colors = [Color(hex_color)  for hex_color in color_list]
        self.css_colors = self.fetch_css_colors()

    @property
    def brightest_color(self):
        return max(self.colors, key=lambda color: color.brightness)

    @staticmethod
    def fetch_css_colors():
        response = requests.get(CSS_COLORS_API_BASE_URL)
        if response.status_code == 200:
            colors_data = response.json().get("colors", [])
            filtered_colors = [
                CSSColor(name=color.get("name"), hex=color.get("hex"), rgb=color.get("rgb"))
                for color in colors_data
            ]
            return filtered_colors
        return []


    def _find_closest_color(self, color: Color) -> str:
        min_distance = float("inf")
        closest_color_name = "Unknown"

        for css_color in self.fetch_css_colors():
            css_rgb = np.fromstring(css_color.rgb, dtype=int, sep=',')
            distance = np.linalg.norm(np.array(css_rgb) - np.array((color.r, color.g, color.b)))

            if distance < min_distance:
                min_distance = distance
                closest_color_name = css_color.name

        return closest_color_name

    def get_brightest_color_info(self) -> str:
        return (f'The brightest color is:  '
                f'{self.brightest_color.hex_value} '
                f'(r={self.brightest_color.r}, '
                f'g={self.brightest_color.g}, '
                f'b={self.brightest_color.b}), '
                f'called {self._find_closest_color(self.brightest_color)}')
