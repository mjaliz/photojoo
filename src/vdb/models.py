from pydantic import BaseModel


class ProductMetadata(BaseModel):
    name: str = ""
    category_name: str = ""
    current_price: float = 0
    image_url: str


class ProductEmbed(BaseModel):
    id: str
    values: list[float]
    metadata: ProductMetadata
