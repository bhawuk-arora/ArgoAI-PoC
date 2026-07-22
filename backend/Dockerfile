FROM python:3.10-slim

WORKDIR /app

# Copy and install dependencies
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and data
# Note: since this is built from the docker-compose at the root, the context is the root directory
COPY backend/ backend/
COPY data/ data/

WORKDIR /app/backend

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
