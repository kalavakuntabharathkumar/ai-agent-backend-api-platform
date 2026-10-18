from uuid import uuid4
from .models import AgentRecord, RunRecord, now_iso
class InMemoryStore:
    def __init__(self):
        self.agents: dict[str, AgentRecord] = {}
        self.runs: dict[str, RunRecord] = {}
        self.seed()
    def seed(self):
        agent = AgentRecord(id="agent-demo", name="demo-agent", description="Deterministic example agent",
                            enabled=True, created_at=now_iso())
        self.agents[agent.id] = agent
    def create_agent(self, name, description="", enabled=True):
        record = AgentRecord(id=f"agt_{uuid4().hex[:10]}", name=name, description=description,
                             enabled=enabled, created_at=now_iso())
        self.agents[record.id] = record
        return record
    def create_run(self, agent_id, payload, max_attempts):
        record = RunRecord(id=f"run_{uuid4().hex[:10]}", agent_id=agent_id, status="queued",
            input=payload, max_attempts=max_attempts, created_at=now_iso(), updated_at=now_iso())
        self.runs[record.id] = record
        return record
store = InMemoryStore()
