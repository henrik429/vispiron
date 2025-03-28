from fastapi import FastAPI, HTTPException
from backend.app.services import ColorService
from backend.app.models import ColorRequest
import re
app = FastAPI(title="Hex Color Brightness API")

@app.get("/")
def root():
    return {"message": "Hello Hex Color Brightness API"}


@app.post("/brightest_color/")
def get_brightest_color(color_request: ColorRequest):
    if not color_request.colors:
        raise HTTPException(status_code=400, detail="Color list cannot be empty.")

    for hex_color in color_request.colors:
        if not re.fullmatch(r"^#([A-Fa-f0-9]{6})$", hex_color):
            raise HTTPException(status_code=400, detail= f'Invalid hex color "{hex_color}"! Allowed characters after "#": 0-9, A-F, a-f and must start with "#" and be 7 characters long.')

    brightest = ColorService(color_request.colors).get_brightest_color_info()
    return {"brightest_color": brightest}
