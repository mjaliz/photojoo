from pydantic import BaseModel


class ProductDoc(BaseModel):
    id: str
    title: str
    category_name: str
    current_price: float
    image_url: str
