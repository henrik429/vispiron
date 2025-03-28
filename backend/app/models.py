from pydantic import BaseModel
from typing import List

class ColorRequest(BaseModel):
    colors: List[str]

class CSSColor(BaseModel):
    name: str
    hex: str
    rgb: str