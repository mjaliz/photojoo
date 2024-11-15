import os
from pydantic import TypeAdapter
from meilisearch import Client
from meilisearch.models.index import IndexStats
from src.meili.model import ProductDoc


class Meili:
    def __init__(self):
        self._client = Client(os.environ.get("MEILI_HOST"), "masterKey")
        self._index = self._client.index("products")

    def add_documents(self, documents: list[ProductDoc]):
        self._index.add_documents([p.model_dump() for p in documents])
        self._index.update_filterable_attributes(
            [
                "category_name",
                "current_price",
            ]
        )

    def search(self, query: str, filter: str | None = None) -> list[ProductDoc]:
        res = self._index.search(query, {"filter": filter})
        return TypeAdapter(list[ProductDoc]).validate_python(res.get("hits"))

    def index_stats(self) -> IndexStats:
        return self._index.get_stats()
