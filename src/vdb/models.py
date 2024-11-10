from pydantic import BaseModel


class ProductMetadata(BaseModel):
    category_name: str | None = None
    current_price: float | None = None
    image_url: str


class ProductEmbed(BaseModel):
    id: str
    values: list[float]
    metadata: ProductMetadata
