FROM python:3.9.1

WORKDIR /app

COPY setup.py .

RUN pip install -e .[dev]

COPY . .

