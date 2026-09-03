FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY . .
RUN uv sync --frozen && uv run python -m spacy download en_core_web_sm
RUN mkdir -p /app/data

EXPOSE 8111
CMD ["uv", "run", "python", "run.py"]