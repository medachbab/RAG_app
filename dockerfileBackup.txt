FROM python:3.13.9-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1\
PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y curl

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN uv --version
COPY ./backend_django/requirement.txt .

RUN uv pip install -r requirement.txt --system || (cat requirement.txt && exit 1)

COPY ./backend_django/ .
EXPOSE 8000
CMD ["./entrypoint.sh"]


