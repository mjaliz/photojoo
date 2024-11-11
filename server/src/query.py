from pydantic import BaseModel, Field


class SearchFilter(BaseModel):
    query: str
    category_name: str | None = None
    price_gte: float | None = Field(default=None, gte=0)
    price_lte: float | None = Field(default=None, gte=0)
