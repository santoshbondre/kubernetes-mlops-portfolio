FROM python:3.11-slim

WORKDIR /app

COPY rag_app.py ./

RUN pip install --no-cache-dir fastapi uvicorn requests

EXPOSE 8000

CMD ["uvicorn", "rag_app:app", "--host", "0.0.0.0", "--port", "8000"]
