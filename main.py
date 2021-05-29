import io
from uuid import uuid4

import httpx
import numpy as np
from PIL import Image

from uvicorn.config import logger
from fastapi import FastAPI, File

app = FastAPI()


def read_image(image: bytes) -> np.ndarray:
    arr = np.array(Image.open(io.BytesIO(image)))
    return arr


def make_package(image_arr: np.ndarray) -> dict:
    return {
        "model": "facedet-retinaface",
        "source_id": str(uuid4()),
        "inputs": [
            {
                "shape": image_arr.shape,
                "datatype": "uint8",
                "data": image_arr.ravel().tolist(),
                "parameters": {},
            },
        ],
    }


async def process(package: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://inferoxy:8698/infer", json=package, timeout=None
        )
    result = response.json()
    return result


async def count_peoples(image: bytes) -> int:
    image_arr = read_image(image)
    json_package = make_package(image_arr)
    result = await process(json_package)
    logger.info(f"Result {result['outputs'][0]['output']}")
    peoples = 1
    return peoples


@app.post("/count")
async def count_peoples_route(image: bytes = File(...)):
    peoples_number = await count_peoples(image)
    return {"peoples": peoples_number}
