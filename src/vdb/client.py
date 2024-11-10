from pinecone.grpc import PineconeGRPC, GRPCClientConfig

from src.vdb.models import ProductEmbed


# Initialize a client. An API key must be passed, but the
# value does not matter.
class VDBClient:
    def __init__(self):
        self._pc = PineconeGRPC(api_key="pclocal")
        self._index = self._pc.Index(
            host="localhost:5081", grpc_config=GRPCClientConfig(secure=False)
        )

    def upsert(self, item: ProductEmbed):
        # vector = item.model_dump()
        self._index.upsert(
            vectors=[
                item,
            ],
            namespace="products",
        )

    def query(self, emb, filter, k=5):
        return self._index.query(
            vector=emb,
            filter=filter,
            top_k=k,
            include_values=True,
            include_metadata=True,
            namespace="products",
        )
