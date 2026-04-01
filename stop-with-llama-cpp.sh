#!/bin/bash

# Stop llama-cpp Podman container if running
if podman ps --format '{{.Names}}' | grep -q '^llama-cpp$'; then
  echo "Stopping llama-cpp container..."
  podman stop llama-cpp
else
  echo "llama-cpp container is not running."
fi

# Stop the rest of the stack
if [ -f docker-compose.yml ]; then
  docker compose down
else
  echo "docker-compose.yml not found. Skipping docker compose down."
fi
