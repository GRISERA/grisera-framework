from typing import Optional, Any
from pydantic import BaseModel


class MinimalRoleModelIn(BaseModel):
    role_name: Optional[str]
    src_instance_name: Optional[str]


class ObjectPropertyRoleModelIn(MinimalRoleModelIn):
    dst_instance_name: Optional[str]


class DataTypePropertyRoleModelIn(MinimalRoleModelIn):
    value: Optional[Any]


class MinimalRoleModelOut(BaseModel):
    links: Optional[str]
    role_name: Optional[str]
    src_instance_name: Optional[str]
    errors: Optional[str]


class ObjectPropertyRoleModelOut(MinimalRoleModelOut):
    dst_instance_name: Optional[str]


class DataTypePropertyRoleModelOut(MinimalRoleModelOut):
    value: Optional[Any]
