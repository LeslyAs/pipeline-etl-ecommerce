FROM python:3.11-slim

WORKDIR /app

RUN pip install psycopg2-binary

COPY load.py .

CMD ["python", "load.py"]