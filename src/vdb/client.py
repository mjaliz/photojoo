import itertools
import os
from pinecone.grpc import PineconeGRPC, GRPCClientConfig
from pinecone import Pinecone

from src.vdb.models import ProductEmbed


class VDBClient:
    def __init__(self):
        self._pc = PineconeGRPC(api_key="pclocal")
        self._host = os.environ["VDB_HOST"]
        self._index = self._pc.Index(
            host=self._host, grpc_config=GRPCClientConfig(secure=False)
        )
        # self._pc = Pinecone(api_key=os.environ["VDB_API_KEY"])
        # self._pc.Index("photojoo")

    @staticmethod
    def _chunks(iterable, batch_size=500):
        it = iter(iterable)
        chunk = tuple(itertools.islice(it, batch_size))
        while chunk:
            yield chunk
            chunk = tuple(itertools.islice(it, batch_size))

    def upsert(self, item: ProductEmbed):
        self._index.upsert(
            vectors=[
                item.model_dump(),
            ],
            namespace="products",
        )

    def batch_upsert(self, items: list[dict]):
        for ids_vectors_chunk in self._chunks(items):
            self._index.upsert(vectors=ids_vectors_chunk, namespace="products")

    def query(self, emb: list[float], filter: dict | None = None, k=10):
        return self._index.query(
            vector=emb,
            filter=filter,
            top_k=k,
            include_metadata=True,
            namespace="products",
        )

    def describe_index_stats(self):
        return self._index.describe_index_stats()
