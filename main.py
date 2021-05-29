import io

import numpy as np
from PIL import Image

from fastapi import FastAPI, File

app = FastAPI()


def read_image(image: bytes) -> np.ndarray:
    arr = np.array(Image.open(io.BytesIO(image)))
    return arr


def make_package(image_arr: np.ndarray) -> dict:
    return {}


def process(package: dict) -> dict:
    return {"outputs": [{"output": {"faces": [1, 2, 3]}}]}


def count_peoples(image: bytes) -> int:
    image_arr = read_image(image)
    json_package = make_package(image_arr)
    result = process(json_package)
    peoples = len(result["outputs"][0]["output"]["faces"])
    return peoples


@app.post("/count")
async def count_peoples_route(image: bytes = File(...)):
    peoples_number = count_peoples(image)
    return {"peoples": peoples_number}
