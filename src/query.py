from pydantic import BaseModel, Field


class SearchFilter(BaseModel):
    query: str
    category_name: str | None = None
    price_lte: float | None = Field(default=None, gt=0)
    price_gte: float | None = Field(default=None, gt=0)
