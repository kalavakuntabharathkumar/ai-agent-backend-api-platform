from fastapi.testclient import TestClient
from agent_platform.main import app
from agent_platform.store import store
client = TestClient(app)
def setup_function():
    store.agents.clear(); store.runs.clear(); store.seed()
def test_health_ready_version():
    assert client.get("/health").status_code == 200
    assert client.get("/ready").json()["ready"]
    assert client.get("/version").json()["version"] == "0.1.0"
def test_agent_crud():
    res = client.post("/agents", json={"name": "researcher", "description": "Search docs"})
    assert res.status_code == 201
    aid = res.json()["id"]
    assert client.get(f"/agents/{aid}").status_code == 200
    assert client.patch(f"/agents/{aid}", json={"enabled": False}).json()["enabled"] is False
    assert client.delete(f"/agents/{aid}").status_code == 204
    assert client.get(f"/agents/{aid}").status_code == 404
def test_run_and_metrics():
    res = client.post("/runs", json={"agent_id": "agent-demo", "input": {"question": "hello"}})
    assert res.status_code == 201 and res.json()["status"] == "succeeded"
    rid = res.json()["id"]
    assert client.get(f"/runs/{rid}").status_code == 200
    assert client.get("/runs").status_code == 200
    assert client.get("/metrics").json()["runs"] == 1
def test_unknown_and_disabled_agents():
    assert client.post("/runs", json={"agent_id": "missing", "input": {}}).status_code == 404
    store.agents["agent-demo"] = store.agents["agent-demo"].model_copy(update={"enabled": False})
    assert client.post("/runs", json={"agent_id": "agent-demo", "input": {}}).status_code == 409
