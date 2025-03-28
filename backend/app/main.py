from fastapi import FastAPI, HTTPException
from app.services import ColorService
from app.models import ColorRequest

app = FastAPI(title="Hex Color Brightness API")

@app.get("/")
def root():
    return {"message": "Hello Hex Color Brightness API"}


@app.post("/brightest_color/")
def get_brightest_color(color_request: ColorRequest):
    if not color_request.colors:
        raise HTTPException(status_code=400, detail="Color list cannot be empty.")

    brightest = ColorService(color_request.colors).get_brightest_color_info()
    return {"brightest_color": brightest}
