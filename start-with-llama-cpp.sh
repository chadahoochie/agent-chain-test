#!/bin/bash

# Start llama-cpp server in the background
podman run --rm -d \
  --name llama-cpp \
  -p 8000:8000 \
  -v $(pwd)/models:/models:Z \
  ghcr.io/abetlen/llama-cpp-python:latest \
  python3 -m llama_cpp.server --model /models/codellama-13b.Q4_K_M.gguf --host 0.0.0.0 --port 8000

# Wait for llama-cpp to be ready (simple sleep, adjust as needed)
sleep 10

# Start the rest of the stack
exec docker compose up
