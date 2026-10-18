from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, Field
def now_iso(): return datetime.now(timezone.utc).isoformat()
class AgentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    description: str = Field(default="", max_length=500)
    enabled: bool = True
class AgentPatch(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=80)
    description: str | None = Field(default=None, max_length=500)
    enabled: bool | None = None
class AgentRecord(BaseModel):
    id: str
    name: str
    description: str = ""
    enabled: bool = True
    created_at: str
class RunCreate(BaseModel):
    agent_id: str
    input: dict = Field(default_factory=dict)
    max_attempts: int = Field(default=3, ge=1, le=3)
class RunRecord(BaseModel):
    id: str
    agent_id: str
    status: Literal["queued", "running", "succeeded", "failed", "cancelled"]
    input: dict
    output: dict = Field(default_factory=dict)
    error: str | None = None
    attempts: int = 0
    max_attempts: int = 3
    created_at: str
    updated_at: str
