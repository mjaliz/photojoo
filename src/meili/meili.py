from meilisearch import Client
from meilisearch.models.index import IndexStats
from src.meili.model import ProductDoc


class Meili:
    def __init__(self):
        self._client = Client("http://127.0.0.1:7700", "masterKey")
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
        return res.get("hits")

    def index_stats(self) -> IndexStats:
        return self._index.get_stats()
