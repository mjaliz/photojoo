FROM ghcr.io/astral-sh/uv:python3.10-bookworm
WORKDIR /app
COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen
COPY . /app/
EXPOSE 8000
CMD [ "uv","run","uvicorn", "src.main:app", "--host","0.0.0.0" ]
# comment