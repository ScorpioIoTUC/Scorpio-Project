FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /entrypoints

COPY src/entrypoints/requirements.txt /entrypoints/requirements.txt
RUN pip install --no-cache-dir -r /entrypoints/requirements.txt

COPY src /entrypoints/src
COPY configs /entrypoints/configs

CMD ["python", "/entrypoints/src/entrypoints/data_ingest.py"]
