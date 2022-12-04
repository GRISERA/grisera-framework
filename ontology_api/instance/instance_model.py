from pydantic import BaseModel
from typing import Optional, Any

class MinimalInstanceModelIn(BaseModel):
    name: Optional[str]


class InstanceModelIn(BaseModel):
    name: str
    class_name: str


class FullInstanceModelIn(BaseModel):
    name: str
    class_name: str
    model_id: int
