import json
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path
from pydantic import BaseModel, TypeAdapter
from torch import cat

from src.clip import CLIP
from src.vdb import VDBClient
from src.vdb.models import ProductEmbed, ProductMetadata


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

    c = CLIP()
    vdb = VDBClient()
    products = Products.validate_python(data)
    products_100 = products[:100]
    for product in products_100:
        img = get_image(product.images[0])
        img_emb = c.image_embedding(img).tolist()[0]
        product_emb = {
            "id": str(product.id),
            "values": img_emb,
            "metadata": {
                "category_name": product.category_name,
                "current_price": product.current_price,
                "image_url": product.images[0],
            },
        }
        vdb.upsert(product_emb)

    response = vdb.query(c.text_embedding("A green woman dress designed with flowers"))
    print(response)
