from fastapi import FastAPI
from PIL import Image

app = FastAPI()

def detect_image(image: Image.Image):
    return {
        "width": image.width,
        "height": image.height,
        "mode": image.mode,
    }