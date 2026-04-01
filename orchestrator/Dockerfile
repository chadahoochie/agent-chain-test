# Orchestrator Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install grpcio grpcio-tools protobuf
EXPOSE 8080
CMD ["python", "orchestrator.py"]
