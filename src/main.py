from typing import Annotated
from fastapi import FastAPI, Request, Query, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from pinecone.core.openapi.data.model.query_response import QueryResponse
from loguru import logger
from meilisearch.errors import MeilisearchApiError

from src.clip import CLIP
from src.vdb import VDBClient, seed_vdb
from src.query import SearchFilter
from src.meili import Meili, seed_meili


@asynccontextmanager
async def lifespan(app: FastAPI):
    data_len_to_insert = 50
    vdb = VDBClient()
    stats = vdb.describe_index_stats()
    vec_count = stats.get("total_vector_count")
    if vec_count == 0:
        logger.info("no vector found in db")
        seed_vdb(vdb, length=data_len_to_insert)
    meili = Meili()
    try:
        meili_stats = meili.index_stats()
        if meili_stats.number_of_documents == 0:
            logger.info("no doc found in meili")
            seed_meili(meili, length=data_len_to_insert)
    except MeilisearchApiError:
        logger.info("no doc found in meili")
        seed_meili(meili, length=data_len_to_insert)
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
    meili: Annotated[Meili, Depends(Meili)],
):
    query = search_filter.query
    if (
        search_filter.price_gte is not None
        and search_filter.price_lte is not None
        and search_filter.price_gte > search_filter.price_lte
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect price filter"
        )
    query_filters = []
    query_filter = None
    meili_filter = ""
    if search_filter.category_name is not None:
        query_filters.append({"category_name": {"$eq": search_filter.category_name}})
        meili_filter += f"category_name = {search_filter.category_name}"
    if search_filter.price_gte is not None:
        query_filters.append({"current_price": {"$gte": search_filter.price_gte}})
        meili_filter += f"{' AND' if meili_filter!='' else ''}current_price >= {search_filter.price_gte}"
    if search_filter.price_lte is not None:
        query_filters.append({"current_price": {"$lte": search_filter.price_lte}})
        meili_filter += f" AND current_price <= {search_filter.price_lte}"
    if len(query_filters) > 0:
        query_filter = {"$and": [*query_filters]}
    clip: CLIP = request.app.state.clip
    query_emb = clip.text_embedding(query)
    res: QueryResponse = vdb.query(query_emb, filter=query_filter)
    meili_res = meili.search(query, filter=meili_filter)
    return res.to_dict()
