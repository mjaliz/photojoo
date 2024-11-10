from pydantic import BaseModel, Field


class SearchFilter(BaseModel):
    query: str
    category_name: str | None = None
    current_price: float | None = Field(default=None, gt=0)
