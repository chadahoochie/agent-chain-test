# Review Agent gRPC Service (Skeleton)
import grpc
from concurrent import futures
import time
import os

try:
    from . import agent_pb2
    from . import agent_pb2_grpc
except ImportError:
    import agent_pb2
    import agent_pb2_grpc
import requests
import json

# Model client abstraction
class ModelClient:
    def __init__(self):
        self.provider = os.environ.get("MODEL_PROVIDER", "local_llama")
        self.endpoint = os.environ.get("MODEL_ENDPOINT", "http://localhost:8004/v1/chat/completions")
        self.model_name = os.environ.get("MODEL_NAME", "llama-2-13b")

    def query_model(self, prompt):
        headers = {"Content-Type": "application/json"}
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are a professional at reviewing code and pointing out flaws. Return a JSON list of review comments with line and comment."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
        try:
            resp = requests.post(self.endpoint, headers=headers, data=json.dumps(data), timeout=60)
            resp.raise_for_status()
            result = resp.json()
            content = result["choices"][0]["message"]["content"]
            return json.loads(content)
        except Exception as e:
            return {"error": str(e)}

    def review_code(self, code_path, context):
        try:
            with open(code_path, "r") as f:
                code = f.read()
        except Exception as e:
            return {"error": f"Failed to read code: {e}"}
        prompt = f"Review the following C# code and point out flaws. Return review comments as JSON.\n\n{code}"
        return self.query_model(prompt)

class ReviewAgent(agent_pb2_grpc.AgentServiceServicer):
    def __init__(self):
        self.model = ModelClient()
    def ProcessTask(self, request, context):
        result = self.model.review_code(request.code_path, request.context)
        return agent_pb2.AgentResult(
            task_id=request.task_id,
            success=True,
            output=str(result),
            error=""
        )
    def GetState(self, request, context):
        # TODO: Implement persistent state retrieval
        return agent_pb2.StateResponse(key=request.key, value="")
    def SetState(self, request, context):
        # TODO: Implement persistent state update
        return agent_pb2.AgentResult(task_id="", success=True, output="", error="")
    def HealthCheck(self, request, context):
        return agent_pb2.AgentResult(task_id="", success=True, output="OK", error="")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    agent_pb2_grpc.add_AgentServiceServicer_to_server(ReviewAgent(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Review Agent running on port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
