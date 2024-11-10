import itertools
from pinecone.grpc import PineconeGRPC, GRPCClientConfig

from src.vdb.models import ProductEmbed


# Initialize a client. An API key must be passed, but the
# value does not matter.
class VDBClient:
    def __init__(self, host: str):
        self._pc = PineconeGRPC(api_key="pclocal")
        self._host = host
        self._index = self._pc.Index(
            host=host, grpc_config=GRPCClientConfig(secure=False)
        )

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

    def batch_upsert(self, items: list[ProductEmbed]):
        with self._pc.Index(host=self._host, pool_threads=30) as index:
            # Send requests in parallel
            async_results = [
                index.upsert(vectors=ids_vectors_chunk, async_req=True)
                for ids_vectors_chunk in self._chunks(items)
            ]
            # Wait for and retrieve responses (this raises in case of error)
            [async_result.get() for async_result in async_results]

    def query(self, emb, filter, k=5):
        return self._index.query(
            vector=emb,
            filter=filter,
            top_k=k,
            include_values=True,
            include_metadata=True,
            namespace="products",
        )
