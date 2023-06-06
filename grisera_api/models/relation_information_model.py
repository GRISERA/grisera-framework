from typing import Optional, Union
from pydantic import BaseModel


class RelationInformation(BaseModel):
    """
    Simplified model of relation, which passes information

    Attributes:
        value: [Optional]([Union](int, str)) name or value of second instance
        second_node_id (int): ID of second node of relation. It can be start node or end node.
        relation_id (int): ID of relationship from database.
        name (str): Name of relationship.
    """
    value: Optional[Union[int, str]]
    second_node_id: int
    relation_id: int
    name: str
