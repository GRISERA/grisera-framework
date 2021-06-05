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


class BasicNodeOut(NodeIn):
    """
    Model of node in database

    Attributes:
        id (Optional[int]): Id of node returned from graph database
        propeties(Optional[List[PropertyIn]]): List of properties of the node in the database
    """
    id: Optional[int]
    properties: Optional[List[PropertyIn]] = None


class NodeOut(BasicNodeOut):
    """
    Model of node to send to client as a result of request

    Attributes:
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list): Hateoas implementation
    """
    errors: Optional[Any] = None
    links: Optional[list] = None


class NodesOut(BaseModel):
    """
    Model of list of nodes

    Attributes:
        nodes (Optional[List[BasicNodeOut]]): List of nodes to send
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list): Hateoas implementation
    """
    nodes: Optional[List[BasicNodeOut]] = None
    errors: Optional[Any] = None
    links: Optional[List] = None
