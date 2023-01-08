from pydantic import BaseModel
from typing import Optional, Any

class MinimalInstanceModelIn(BaseModel):
    name: Optional[str]


class InstanceModelIn(MinimalInstanceModelIn):
    class_name: Optional[str]


class FullInstanceModelIn(InstanceModelIn):
    model_id: Optional[int]


class MinimalModelOut(BaseModel):
    errors: Optional[str]
