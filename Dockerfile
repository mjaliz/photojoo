FROM ghcr.io/astral-sh/uv:python3.10-bookworm
WORKDIR /app
COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen
COPY . /app/
CMD [ "uvicorn", "src.main:app" ]