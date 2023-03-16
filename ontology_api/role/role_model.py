from typing import Optional, Union
from pydantic import BaseModel


class RoleModelIn(BaseModel):
    role: Optional[str]
    instance_name: Optional[str]
    value: Union[str, int, None]


class RoleModelOut(RoleModelIn):
    links: Optional[str]
    errors: Optional[str]
