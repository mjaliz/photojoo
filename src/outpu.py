from pydantic import BaseModel

from src.vdb.models import ProductMetadata


class Match(BaseModel):
    id: str
    metadata: ProductMetadata


class ProductOutput(BaseModel):
    matches: list[Match]
