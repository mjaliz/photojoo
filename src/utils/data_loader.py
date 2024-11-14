import json
from pathlib import Path
from pydantic import BaseModel, TypeAdapter


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


def load_json_data() -> list[Product]:
    with open(DATA_PATH.resolve(), "r") as f:
        data = json.loads(f.read())
    return Products.validate_python(data)
