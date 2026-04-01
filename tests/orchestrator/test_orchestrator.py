from orchestrator import orchestrator as mut


class FakeChannel:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_call_agent_uses_stub_and_returns_response(monkeypatch):
    seen = {}

    def fake_insecure_channel(address):
        seen["address"] = address
        return FakeChannel()

    class FakeStub:
        def __init__(self, channel):
            seen["channel"] = channel

        def ProcessTask(self, task):
            seen["task"] = task
            return "ok-response"

    monkeypatch.setattr(mut.grpc, "insecure_channel", fake_insecure_channel)
    monkeypatch.setattr(mut.agent_pb2_grpc, "AgentServiceStub", FakeStub)

    task = object()
    result = mut.call_agent("analyzer_agent:50051", task)

    assert result == "ok-response"
    assert seen["address"] == "analyzer_agent:50051"
    assert seen["task"] is task


def test_main_builds_task_calls_analyzer_and_prints(monkeypatch, capsys):
    seen = {}

    def fake_task_ctor(**kwargs):
        seen["task_kwargs"] = kwargs
        return {"constructed": True, **kwargs}

    def fake_call_agent(address, task):
        seen["address"] = address
        seen["task"] = task
        return "analysis"

    monkeypatch.setattr(mut.agent_pb2, "AgentTask", fake_task_ctor)
    monkeypatch.setattr(mut, "call_agent", fake_call_agent)

    mut.main()

    assert seen["address"] == "analyzer_agent:50051"
    assert seen["task"]["task_id"] == "1"
    assert seen["task"]["code_path"] == "/code"
    output = capsys.readouterr().out
    assert "Analyzer result:" in output
    assert "analysis" in output


def test_main_propagates_call_agent_error(monkeypatch):
    monkeypatch.setattr(mut.agent_pb2, "AgentTask", lambda **kwargs: kwargs)

    def fake_call_agent(_address, _task):
        raise RuntimeError("boom")

    monkeypatch.setattr(mut, "call_agent", fake_call_agent)

    try:
        mut.main()
        raise AssertionError("expected RuntimeError")
    except RuntimeError as exc:
        assert str(exc) == "boom"
