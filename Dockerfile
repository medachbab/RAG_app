FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1\
PYTHONUNBUFFERED=1\
PORT=8000
WORKDIR /app

RUN apt-get update && apt-get install -y curl dos2unix
#forcer l'installation de pytorch version cpu only pour avoir une image lightweight
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

COPY ./backend_django/requirement.txt .

RUN pip install --no-cache-dir -r requirement.txt

COPY ./backend_django/ .

RUN dos2unix entrypoint.sh && chmod +x entrypoint.sh
EXPOSE $PORT
CMD ["./entrypoint.sh"]


