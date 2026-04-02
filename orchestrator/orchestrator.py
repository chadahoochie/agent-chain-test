# Orchestrator gRPC Client (Skeleton)
import grpc
import os
import time
from pathlib import Path
try:
    from . import agent_pb2
    from . import agent_pb2_grpc
except ImportError:  # pragma: no cover - used when running as a direct script
    import agent_pb2
    import agent_pb2_grpc

RPC_TIMEOUT_SECONDS = float(os.environ.get("ORCHESTRATOR_RPC_TIMEOUT_SECONDS", "10"))
RPC_MAX_RETRIES = int(os.environ.get("ORCHESTRATOR_RPC_MAX_RETRIES", "30"))
RPC_RETRY_DELAY_SECONDS = float(os.environ.get("ORCHESTRATOR_RPC_RETRY_DELAY_SECONDS", "1"))
DEFAULT_CODE_PATH = os.environ.get(
    "ORCHESTRATOR_CODE_PATH", "/workspace/agent_chain_controller.py"
)
DEFAULT_OUTPUT_FILE = os.environ.get(
    "ORCHESTRATOR_OUTPUT_FILE", "/state/last_orchestrator_output.txt"
)


def call_agent(address, task):
    with grpc.insecure_channel(address) as channel:
        stub = agent_pb2_grpc.AgentServiceStub(channel)
        last_error = None
        for attempt in range(1, RPC_MAX_RETRIES + 1):
            try:
                response = stub.ProcessTask(
                    task,
                    timeout=RPC_TIMEOUT_SECONDS,
                    wait_for_ready=True,
                )
                return response
            except grpc.RpcError as exc:
                last_error = exc
                if attempt == RPC_MAX_RETRIES:
                    break
                time.sleep(RPC_RETRY_DELAY_SECONDS)

        raise RuntimeError(
            f"Failed to call agent at {address} after {RPC_MAX_RETRIES} attempts"
        ) from last_error


def persist_output(text):
    output_path = Path(DEFAULT_OUTPUT_FILE)
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(f"{text}\n", encoding="utf-8")
        print(f"Wrote orchestrator output to: {output_path}")
    except Exception as exc:  # pragma: no cover - best-effort persistence
        print(f"Warning: failed to write orchestrator output: {exc}")

def main():
    # Example: orchestrate all agents in sequence
    task = agent_pb2.AgentTask(
        task_id="1",
        type=agent_pb2.ANALYZE,
        code_path=DEFAULT_CODE_PATH,
        context="{}",
    )
    analyzer_result = call_agent("analyzer_agent:50051", task)
    print("Analyzer result:", analyzer_result)
    persist_output(analyzer_result)
    # ...repeat for optimizer, test, review agents, passing context/output as needed

if __name__ == "__main__":  # pragma: no cover - script entrypoint
    main()
