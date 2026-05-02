FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/entrypoints

WORKDIR /entrypoints

RUN pip install --no-cache-dir paho-mqtt

COPY src /entrypoints/src
COPY configs /entrypoints/configs

CMD ["python", "-m", "src.entrypoints.data_storage"]
