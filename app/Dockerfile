# =========================
# Base image
# =========================
FROM python:3.10-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean


COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt


COPY . .


RUN mkdir -p /app/media /app/staticfiles


EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
