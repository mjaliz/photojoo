from typing import Annotated
from fastapi import FastAPI, Request, Query, Depends
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from pinecone.core.openapi.data.model.query_response import QueryResponse
from loguru import logger


from server.src.clip import CLIP
from server.src.vdb import VDBClient, seed_vdb
from server.src.query import SearchFilter


@asynccontextmanager
async def lifespan(app: FastAPI):
    vdb = VDBClient()
    stats = vdb.describe_index_stats()
    vec_count = stats.get("total_vector_count")
    if vec_count == 0:
        logger.info("no vector found in db")
        logger.info("seeding vector database...")
        seed_vdb()
        logger.info("seeding vdb done.")
    app.state.clip = CLIP()
    yield
    logger.info("shutting down...")


app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)


@app.get("/search/")
def search_image(
    request: Request,
    search_filter: Annotated[SearchFilter, Query()],
    vdb: Annotated[VDBClient, Depends(VDBClient)],
):
    query = search_filter.query
    query_filters = []
    query_filter = None
    if search_filter.category_name is not None:
        query_filters.append({"category_name": {"$eq": search_filter.category_name}})
    if search_filter.price_gte is not None:
        query_filters.append({"current_price": {"$gte": search_filter.price_gte}})
    if search_filter.price_lte is not None:
        query_filters.append({"current_price": {"$lte": search_filter.price_lte}})
    if len(query_filters) > 0:
        query_filter = {"$and": [*query_filters]}
    clip: CLIP = request.app.state.clip
    query_emb = clip.text_embedding(query)
    res: QueryResponse = vdb.query(query_emb, filter=query_filter)
    return res.to_dict()
