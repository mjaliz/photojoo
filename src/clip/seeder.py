import json
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path
from pydantic import BaseModel, TypeAdapter

from src.clip import CLIP


class Product(BaseModel):
    id: int
    name: str
    description: str
    material: str | None = None
    rating: int | None = None
    images: list[str]
    code: str
    brand_id: int | None = None
    brand_name: str | None = None
    category_id: int | None = None
    category_name: str | None = None
    gender_id: int | None = None
    gender_name: str | None = None
    shop_id: int
    shop_name: str
    link: str | None = None
    status: str
    colors: list[str] | None = None
    sizes: list[str] | None = None
    region: str
    currency: str
    current_price: float | None = None
    old_price: float | None = None
    off_percent: int | None = None
    update_date: str


Products = TypeAdapter(list[Product])

DATA_DIR = Path(__file__).parent.resolve().joinpath("..", "..", "data")
DATA_PATH = DATA_DIR.joinpath("products (1).json")


def get_image(image_URL):
    response = requests.get(image_URL)
    image = Image.open(BytesIO(response.content)).convert("RGB")
    return image


if __name__ == "__main__":
    with open(DATA_PATH.resolve(), "r") as f:
        data = json.loads(f.read())

    products = Products.validate_python(data)
    product_img = products[0].images[0]
    img = get_image(product_img)
    c = CLIP()
    img_emb = c.image_embedding(img)
    print(img_emb)
