import json
from types import SimpleNamespace

import requests

from agents.analyzer_agent import analyzer_agent as mut


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def test_model_client_query_model_returns_parsed_json_on_success(monkeypatch):
    expected = [{"line": 7, "issue": "n+1", "suggestion": "batch"}]
    payload = {
        "choices": [
            {"message": {"content": json.dumps(expected)}}
        ]
    }

    def fake_post(*args, **kwargs):
        return FakeResponse(payload)

    monkeypatch.setattr(mut.requests, "post", fake_post)

    result = mut.ModelClient().query_model("prompt")

    assert result == expected


def test_model_client_query_model_returns_error_on_request_exception(monkeypatch):
    def fake_post(*args, **kwargs):
        raise requests.exceptions.ConnectionError("down")

    monkeypatch.setattr(mut.requests, "post", fake_post)

    result = mut.ModelClient().query_model("prompt")

    assert "error" in result
    assert "down" in result["error"]


def test_model_client_analyze_code_returns_error_when_file_cannot_be_read(tmp_path):
    missing_file = tmp_path / "missing.cs"

    result = mut.ModelClient().analyze_code(str(missing_file), "{}")

    assert "error" in result
    assert result["error"].startswith("Failed to read code:")


def test_model_client_analyze_code_passes_prompt_to_query_model(tmp_path, monkeypatch):
    code_file = tmp_path / "sample.cs"
    code_file.write_text("class C { }", encoding="utf-8")

    seen = {}

    def fake_query_model(self, prompt):
        seen["prompt"] = prompt
        return {"ok": True}

    monkeypatch.setattr(mut.ModelClient, "query_model", fake_query_model)

    result = mut.ModelClient().analyze_code(str(code_file), "{}")

    assert result == {"ok": True}
    assert "Analyze the following C# code for performance issues" in seen["prompt"]
    assert "class C { }" in seen["prompt"]


def test_analyzer_agent_process_task_returns_agent_result(monkeypatch):
    agent = mut.AnalyzerAgent()

    def fake_analyze_code(code_path, context):
        return {"diagnostics": 1}

    monkeypatch.setattr(agent.model, "analyze_code", fake_analyze_code)

    request = SimpleNamespace(task_id="123", code_path="/tmp/a.cs", context="{}")
    response = agent.ProcessTask(request, context=None)

    assert response.task_id == "123"
    assert response.success is True
    assert response.output == str({"diagnostics": 1})
    assert response.error == ""


def test_analyzer_agent_health_check_returns_ok():
    agent = mut.AnalyzerAgent()
    request = SimpleNamespace(key="any")

    response = agent.HealthCheck(request, context=None)

    assert response.success is True
    assert response.output == "OK"
    assert response.error == ""


def test_analyzer_agent_get_state_returns_empty_value():
    agent = mut.AnalyzerAgent()
    request = SimpleNamespace(key="k1")

    response = agent.GetState(request, context=None)

    assert response.key == "k1"
    assert response.value == ""


def test_analyzer_agent_serve_starts_and_stops_server(monkeypatch):
    class FakeServer:
        def __init__(self):
            self.started = False
            self.stopped_with = None
            self.port = None

        def add_insecure_port(self, port):
            self.port = port

        def start(self):
            self.started = True

        def stop(self, value):
            self.stopped_with = value

    fake_server = FakeServer()
    added = {}

    def fake_add_servicer(servicer, server):
        added["servicer"] = servicer
        added["server"] = server

    def fake_sleep(_):
        raise KeyboardInterrupt()

    monkeypatch.setattr(mut.grpc, "server", lambda executor: fake_server)
    monkeypatch.setattr(mut.agent_pb2_grpc, "add_AgentServiceServicer_to_server", fake_add_servicer)
    monkeypatch.setattr(mut.time, "sleep", fake_sleep)

    mut.serve()

    assert fake_server.started is True
    assert fake_server.port == "[::]:50051"
    assert fake_server.stopped_with == 0
    assert added["server"] is fake_server
    assert isinstance(added["servicer"], mut.AnalyzerAgent)
