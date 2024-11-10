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


if __name__ == "__main__":
    pc = PineconeGRPC(api_key="pclocal")

    # Target the indexes. Use the host and port number along with disabling tls.
    index1 = pc.Index(host="localhost:5081", grpc_config=GRPCClientConfig(secure=False))
    # Upsert records into index1
    index1.upsert(
        vectors=[
            {"id": "vec1", "values": [1.0, 1.5], "metadata": {"genre": "comedy"}},
            {"id": "vec2", "values": [2.0, 1.0], "metadata": {"genre": "drama"}},
            {"id": "vec3", "values": [0.1, 3.0], "metadata": {"genre": "comedy"}},
        ],
        namespace="example-namespace",
    )

    # Check the number of records in each index
    print(index1.describe_index_stats())

    # Query index2 with a metadata filter
    response = index1.query(
        vector=[3.0, -2.0],
        filter={"genre": {"$eq": "documentary"}},
        top_k=1,
        include_values=True,
        include_metadata=True,
        namespace="example-namespace",
    )

    print(response)
