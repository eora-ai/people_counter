import io

import numpy as np
from PIL import Image

from fastapi import FastAPI, File

app = FastAPI()


def read_image(image: bytes) -> np.ndarray:
    arr = np.array(Image.open(io.BytesIO(image)))
    return arr


@app.post("/count")
async def count_peoples(image: bytes = File(...)):
    image_arr = read_image(image)
    return {"shape": image_arr.shape[0]}
