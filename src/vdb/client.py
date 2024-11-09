from pinecone.grpc import PineconeGRPC, GRPCClientConfig
import time

# Initialize a client. An API key must be passed, but the
# value does not matter.
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
    filter={"genre": {"$eq": "comedy"}},
    top_k=1,
    include_values=True,
    include_metadata=True,
    namespace="example-namespace",
)

print(response)
