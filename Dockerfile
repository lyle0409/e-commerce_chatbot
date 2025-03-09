# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY main.py json_tool.py search_online.py search_online_4o.py embedding_data.py recommend.py product_data_3_pages_hoangha.json product_data_with_embeddings.json requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]