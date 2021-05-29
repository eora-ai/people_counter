import io

import numpy as np
from PIL import Image

from fastapi import FastAPI, File

app = FastAPI()


def read_image(image: bytes) -> np.ndarray:
    arr = np.array(Image.open(io.BytesIO(image)))
    return arr


def count_peoples(image: bytes) -> int:
    image_arr = read_image(image)
    return image_arr.shape[0]


@app.post("/count")
async def count_peoples_route(image: bytes = File(...)):
    peoples_number = count_peoples(image)
    return {"peoples": peoples_number}
