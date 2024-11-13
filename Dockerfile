FROM ghcr.io/pinecone-io/pinecone-index:latest as VDB
ENV PORT=5081
ENV INDEX_TYPE=serverless
ENV DIMENSION=512
ENV METRIC=cosine
EXPOSE 5081


FROM ghcr.io/astral-sh/uv:python3.10-bookworm
WORKDIR /app
COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen
COPY . /app/
ENV VDB_HOST=VDB:5081
CMD [ "uv","run","uvicorn", "src.main:app" ]