## Model API Requirements
Each agent expects the model endpoint to be OpenAI-compatible (e.g., llama.cpp, llama-cpp-python, OpenAI API, or similar). The endpoint should support POST requests to `/v1/chat/completions` with the following JSON body:

```
{
	"model": "llama-2-13b",
	"messages": [
		{"role": "system", "content": "...instructions..."},
		{"role": "user", "content": "...code or prompt..."}
	],
	"temperature": 0.2
}
```

The model should return a response with a JSON-formatted answer in the first assistant message. See each agent's code for the expected system prompt and output format.
# README: Agentic AI Chain (gRPC, Containers, Persistent State)

## Overview
This project implements a fully agentic AI chain for C# codebases. Each stage (analyzer, optimizer, tester, reviewer) is a self-contained, persistent agent running in its own container, communicating via gRPC. The orchestrator coordinates the workflow and supports partial runs.

## Architecture
- **protos/agent.proto**: gRPC protocol definition for all agents
- **agents/*_agent/**: Each agent is a containerized gRPC service with persistent state
- **orchestrator/**: Orchestrator container, manages agent workflow
- **docker-compose.yml**: Multi-container orchestration

## How it Works
1. Each agent exposes a gRPC server implementing the shared protocol
2. The orchestrator connects to agents, sends tasks, and passes context/results
3. Agents persist their own state (e.g., SQLite, files)
4. Supports partial runs and robust error handling

## Quick Start
1. Build all containers:
	```sh
	docker-compose build
	```
2. Start the system:
	```sh
	docker-compose up
	```
3. The orchestrator will connect to agents and run the chain

## Model Configuration
Each agent uses a specialized AI model for its domain. By default, agents use a recommended local/containerized model (e.g., CodeLlama, StarCoder). You can override the model provider and endpoint via environment variables:

- `MODEL_PROVIDER`: The model provider to use (e.g., `local_llama`, `openai`, `starcoder`).
- `MODEL_ENDPOINT`: The endpoint for the model (e.g., `http://localhost:8001` or a cloud API endpoint).

To override, set these variables in the agent's Dockerfile or via `docker-compose.yml`:

```yaml
environment:
  - MODEL_PROVIDER=openai
  - MODEL_ENDPOINT=https://api.openai.com/v1/...
```

## Extending
- Implement agent logic in each agent's Python service
- Update `agent.proto` for protocol changes
- Add new agents by creating a new service and updating the orchestrator
- Add new model providers by extending the `ModelClient` abstraction in each agent

## Notes
- This is a skeleton implementation. Fill in agent logic and persistent state as needed.
- Designed for C# but extensible to other languages.
