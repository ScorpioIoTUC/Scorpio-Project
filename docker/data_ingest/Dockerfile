FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/entrypoints

WORKDIR /entrypoints

COPY src /entrypoints/src
COPY configs /entrypoints/configs
COPY requirements.txt /entrypoints/requirements.txt
RUN pip install --no-cache-dir -r /entrypoints/requirements.txt

CMD ["python", "-m", "src.entrypoints.data_ingest"]
