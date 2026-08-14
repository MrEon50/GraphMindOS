from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any
import uuid

class Relationship(BaseModel):
    targetId: str
    relationshipType: str
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    condition: Optional[str] = None

class Topology(BaseModel):
    inputs: List[str] = Field(default_factory=list)
    outputs: List[Relationship] = Field(default_factory=list)

class Execution(BaseModel):
    status: Literal["idle", "running", "failed", "completed"] = "idle"
    payload: Optional[Dict[str, Any]] = None
    processor_ref: Optional[str] = None
    error: Optional[str] = None

class Entropy(BaseModel):
    lifespan: float = 1.0
    decay_rate: float = 0.5
    is_ephemeral: bool = False

class GraphNode(BaseModel):
    nodeId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    kind: Literal["primitive", "intent", "state", "controller"]
    vector: Optional[List[float]] = None
    topology: Topology = Field(default_factory=Topology)
    execution: Execution = Field(default_factory=Execution)
    entropy: Entropy = Field(default_factory=Entropy)
