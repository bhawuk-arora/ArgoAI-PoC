FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application directories
COPY frontend/ frontend/
COPY backend/ backend/
COPY data/ data/

# Switch to backend directory since our command runs from there
# (This ensures paths like "../frontend" and "../data/argo_profiles.pkl" work correctly)
WORKDIR /app/backend

# Expose port
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
