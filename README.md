# AI Agent Backend API Platform
FastAPI portfolio starter with 14 REST endpoints for agent registration, run lifecycle, and operational metrics; includes validation, Pytest, Docker, GitHub Actions CI, and cloud deployment guides.

**Benchmark honesty:** supplied resume figures (2.8s→420ms p95, 5,000 daily requests, 90 users, 210 tests, 88% coverage, 5→1 failed releases/month, three clouds, 3h→12m deployments) are not measured by this starter. Validate with repeatable load tests and coverage reports before presenting them as verified.

## Windows / PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:PYTHONPATH = "src"
uvicorn agent_platform.main:app --reload
```
Docs at `http://127.0.0.1:8000/docs`. Tests: `$env:PYTHONPATH="src"; pytest --cov=agent_platform --cov-report=term-missing`.

Docker: `docker build -t ai-agent-api .` then `docker run --rm -p 8000:8000 ai-agent-api`.

## Endpoints
1. GET `/health`
2. GET `/ready`
3. GET `/agents`
4. POST `/agents`
5. GET `/agents/{agent_id}`
6. PATCH `/agents/{agent_id}`
7. DELETE `/agents/{agent_id}`
8. POST `/runs`
9. GET `/runs`
10. GET `/runs/{run_id}`
11. POST `/runs/{run_id}/retry`
12. POST `/runs/{run_id}/cancel`
13. GET `/metrics`
14. GET `/version`

The executor is deterministic and local: no paid LLM calls or arbitrary code execution. Storage is in-memory and resets on restart. Before production, add PostgreSQL/migrations, authentication and authorization, rate limiting, durable task queue/workers, secrets management, and telemetry. Cloud folders are deployment guides, not proof of live deployment.
