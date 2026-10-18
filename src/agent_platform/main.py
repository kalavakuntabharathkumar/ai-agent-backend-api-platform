from fastapi import FastAPI, HTTPException, Response
from .models import AgentCreate, AgentPatch, AgentRecord, RunCreate, RunRecord, now_iso
from .store import store
app = FastAPI(title="AI Agent Backend API Platform", version="0.1.0",
              description="Demo agent registry and run lifecycle API.")
def agent_or_404(agent_id):
    agent = store.agents.get(agent_id)
    if not agent: raise HTTPException(status_code=404, detail="Agent not found")
    return agent
def run_or_404(run_id):
    run = store.runs.get(run_id)
    if not run: raise HTTPException(status_code=404, detail="Run not found")
    return run
@app.get("/health")
def health(): return {"status": "ok"}
@app.get("/ready")
def ready(): return {"ready": True, "storage": "in-memory-demo"}
@app.get("/agents", response_model=list[AgentRecord])
def list_agents(): return list(store.agents.values())
@app.post("/agents", response_model=AgentRecord, status_code=201)
def create_agent(payload: AgentCreate): return store.create_agent(payload.name, payload.description, payload.enabled)
@app.get("/agents/{agent_id}", response_model=AgentRecord)
def get_agent(agent_id: str): return agent_or_404(agent_id)
@app.patch("/agents/{agent_id}", response_model=AgentRecord)
def patch_agent(agent_id: str, payload: AgentPatch):
    current = agent_or_404(agent_id)
    changes = {k: v for k, v in payload.model_dump(exclude_unset=True).items() if v is not None}
    updated = current.model_copy(update=changes)
    store.agents[agent_id] = updated
    return updated
@app.delete("/agents/{agent_id}", status_code=204)
def delete_agent(agent_id: str):
    agent_or_404(agent_id)
    del store.agents[agent_id]
    return Response(status_code=204)
@app.post("/runs", response_model=RunRecord, status_code=201)
def create_run(payload: RunCreate):
    agent = agent_or_404(payload.agent_id)
    if not agent.enabled: raise HTTPException(status_code=409, detail="Agent is disabled")
    run = store.create_run(payload.agent_id, payload.input, payload.max_attempts)
    run.status, run.attempts = "running", 1
    run.output = {"message": "Demo run completed", "input_keys": sorted(payload.input.keys())}
    run.status, run.updated_at = "succeeded", now_iso()
    store.runs[run.id] = run
    return run
@app.get("/runs", response_model=list[RunRecord])
def list_runs(): return sorted(store.runs.values(), key=lambda r: r.created_at, reverse=True)
@app.get("/runs/{run_id}", response_model=RunRecord)
def get_run(run_id: str): return run_or_404(run_id)
@app.post("/runs/{run_id}/retry", response_model=RunRecord)
def retry_run(run_id: str):
    run = run_or_404(run_id)
    if run.status not in ("failed", "succeeded"): raise HTTPException(status_code=409, detail=f"Cannot retry a {run.status} run")
    if run.attempts >= run.max_attempts: raise HTTPException(status_code=409, detail="Maximum attempts reached")
    run.attempts += 1
    run.status, run.error = "succeeded", None
    run.output = {"message": "Demo retry completed", "input_keys": sorted(run.input.keys())}
    run.updated_at = now_iso()
    store.runs[run.id] = run
    return run
@app.post("/runs/{run_id}/cancel", response_model=RunRecord)
def cancel_run(run_id: str):
    run = run_or_404(run_id)
    if run.status not in ("queued", "running"): raise HTTPException(status_code=409, detail=f"Cannot cancel a {run.status} run")
    run.status, run.updated_at = "cancelled", now_iso()
    store.runs[run.id] = run
    return run
@app.get("/metrics")
def metrics():
    statuses = {}
    for run in store.runs.values(): statuses[run.status] = statuses.get(run.status, 0) + 1
    return {"agents": len(store.agents), "runs": len(store.runs), "runs_by_status": statuses}
@app.get("/version")
def version(): return {"name": "ai-agent-backend-api-platform", "version": app.version}
