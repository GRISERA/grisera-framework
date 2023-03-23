from typing import Optional, Union
from pydantic import BaseModel


class RoleModelIn(BaseModel):
    role: Optional[str]
    instance_name: Optional[str]
    value: Union[str, int, None]

class RolesDeletedOut(BaseModel):
    model_id: Optional[int]
    instance_name: Optional[str]
    links: Optional[str]
    errors: Optional[str]

class RoleModelOut(RoleModelIn):
    links: Optional[str]
    errors: Optional[str]
