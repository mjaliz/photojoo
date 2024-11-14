from pydantic import BaseModel

from src.vdb.models import ProductMetadata


class ProductOutput(BaseModel):
    id: str
    metadata: ProductMetadata
