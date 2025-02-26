FROM python:3.10-slim
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
RUN pip install fastapi uvicorn[standard] requests streamlink
WORKDIR /app
COPY backend/ backend/
COPY frontend/ frontend/
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
