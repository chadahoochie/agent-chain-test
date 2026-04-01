# Analyzer Agent Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install grpcio grpcio-tools protobuf requests
ENV MODEL_PROVIDER=local_llama
ENV MODEL_ENDPOINT=http://localhost:8001
EXPOSE 50051
CMD ["python", "analyzer_agent.py"]
