FROM python:3.11-slim

WORKDIR /app

# On installe la bibliothèque qui permet
# à Python de parler à PostgreSQL
RUN pip install psycopg2-binary

COPY transform.py .

CMD ["python", "transform.py"]