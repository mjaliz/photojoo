from typing import Annotated
from fastapi import FastAPI, Request, Query, Depends
from contextlib import asynccontextmanager
from pinecone.core.openapi.data.model.query_response import QueryResponse
from loguru import logger


from src.clip import CLIP, seed_vdb
from src.vdb import VDBClient
from src.query import SearchFilter


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


@app.get("/search/")
def search_image(
    request: Request,
    search_filter: Annotated[SearchFilter, Query()],
    vdb: Annotated[VDBClient, Depends(VDBClient)],
):
    query = search_filter.query
    clip: CLIP = request.app.state.clip
    query_emb = clip.text_embedding(query)
    res: QueryResponse = vdb.query(query_emb)
    return res.to_dict()
