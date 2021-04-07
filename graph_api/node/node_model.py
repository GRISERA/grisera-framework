from typing import Set, Optional, Any, List
from pydantic import BaseModel
from property.property_model import PropertyIn

class NodeIn(BaseModel):
    """
    Model of node to acquire from client

    Attributes:
        labels (Optional[Set[str]]): Labels added to node in graph DB
    """
    labels: Optional[Set[str]] = []


class NodeOut(NodeIn):
    """
    Model of node to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of node returned from graph database
        propeties(Optional[List[PropertyIn]]): List of properties of the node in the database
        errors (Optional[Any]): Optional errors appeared during query executions
    """
    id: Optional[int]
    properties: Optional[List[PropertyIn]] = None
    errors: Optional[Any] = None
    links: Optional[list] = None

