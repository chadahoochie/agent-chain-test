# Orchestrator gRPC Client (Skeleton)
import grpc
try:
    from . import agent_pb2
    from . import agent_pb2_grpc
except ImportError:  # pragma: no cover - used when running as a direct script
    import agent_pb2
    import agent_pb2_grpc

def call_agent(address, task):
    with grpc.insecure_channel(address) as channel:
        stub = agent_pb2_grpc.AgentServiceStub(channel)
        response = stub.ProcessTask(task)
        return response

def main():
    # Example: orchestrate all agents in sequence
    task = agent_pb2.AgentTask(task_id="1", type=agent_pb2.ANALYZE, code_path="/code", context="{}")
    analyzer_result = call_agent("analyzer_agent:50051", task)
    print("Analyzer result:", analyzer_result)
    # ...repeat for optimizer, test, review agents, passing context/output as needed

if __name__ == "__main__":  # pragma: no cover - script entrypoint
    main()
