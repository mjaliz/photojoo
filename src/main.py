import os
from typing import Annotated
from fastapi import FastAPI, Request, Query, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from pinecone.core.openapi.data.model.query_response import QueryResponse
from loguru import logger
from meilisearch.errors import MeilisearchApiError

from src.clip import CLIP
from src.meili.model import ProductDoc
from src.outpu import ProductOutput, Match
from src.vdb import VDBClient, seed_vdb
from src.query import SearchFilter
from src.meili import Meili, seed_meili


@asynccontextmanager
async def lifespan(app: FastAPI):
    data_len_to_insert = os.environ.get("DATA_LEN")
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

origins = ["*"]

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
    vdb_filters, meili_filters = build_filters(search_filter)

    clip: CLIP = request.app.state.clip
    query_emb = clip.text_embedding(query)

    vdb_res: QueryResponse = vdb.query(query_emb, filter=vdb_filters)
    meili_res = None
    if search_filter.keyword_search:
        meili_res = meili.search(query, filter=meili_filters)

    return combine_search_results(vdb_res, meili_res)


def build_filters(filters: SearchFilter) -> tuple[list[dict] | None, str]:
    if (
        filters.price_gte is not None
        and filters.price_lte is not None
        and filters.price_gte > filters.price_lte
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect price filter"
        )
    query_filters = []
    vdb_filter = None
    meili_filter = ""
    if filters.category_name is not None:
        query_filters.append({"category_name": {"$eq": filters.category_name}})
        meili_filter += f"category_name = {filters.category_name}"
    if filters.price_gte is not None:
        query_filters.append({"current_price": {"$gte": filters.price_gte}})
        meili_filter += (
            f"{' AND ' if meili_filter!='' else ''}current_price >= {filters.price_gte}"
        )
    if filters.price_lte is not None:
        query_filters.append({"current_price": {"$lte": filters.price_lte}})
        meili_filter += f" AND current_price <= {filters.price_lte}"
    if len(query_filters) > 0:
        vdb_filter = {"$and": [*query_filters]}

    return vdb_filter, meili_filter


def combine_search_results(
    vdb_res: QueryResponse,
    meili_res: list[ProductDoc] | None,
) -> ProductOutput:
    vdb_res = vdb_res.to_dict()
    vdb_matches = vdb_res.get("matches")
    ids = []
    results: list[Match] = []
    for vdbm in vdb_matches:
        results.append(Match(**vdbm))
        ids.append(vdbm.get("id"))

    if meili_res is None:
        return ProductOutput(matches=results)

    for mr in meili_res:
        # Check for possibly duplicate results
        if mr.id not in ids:
            results.append(Match(id=mr.id, metadata=mr.model_dump()))

    return ProductOutput(matches=results)
