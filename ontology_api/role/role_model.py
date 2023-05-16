from typing import Optional, Union, List
from pydantic import BaseModel


class RoleModelIn(BaseModel):
    role: Optional[str]
    instance_name: Optional[str]
    value: Union[str, int, None]


class RolesDeletedOut(BaseModel):
    instance_name: Optional[str]
    links: Optional[str]
    errors: Optional[str]


class RoleModelOut(RoleModelIn):
    links: Optional[str]
    errors: Optional[str]


class RolesModelOut(BaseModel):
    roles: List[RoleModelIn] = []
    links: Optional[str]
    errors: Optional[str]