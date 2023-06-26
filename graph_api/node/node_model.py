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


class NodeParameterQueryIn(BaseModel):
    """
    Model of node query to acquire from client
    Attributes:
        key (str): name of parameter
        operator (str): compare operator
        value (str): compared value
    """
    key: str
    operator: str
    value: str


class NodeQueryIn(BaseModel):
    """
    Model of node query to acquire from client
    Attributes:
        id (Optional[int]): id of node in graph DB
        label (Optional[int]): label of node in graph DB
        result bool: return node as result
    """
    id: Optional[int]
    label: Optional[str]
    result = False
    parameters: Optional[List[NodeParameterQueryIn]]


class RelationQueryIn(BaseModel):
    """
    Model of relation query to acquire from client
    Attributes:
        begin_node_index (Optional[int]): id of begin node in relation in graph DB
        end_node_index (Optional[int]): id of end node in relation in graph DB
        min_count (Optional[int]): minimum length of the relation
        label (Optional[int]): label of relation in graph DB
    """
    begin_node_index: Optional[int]
    end_node_index: Optional[int]
    min_count: Optional[int]
    label: Optional[str]


class NodeRowsQueryIn(BaseModel):
    """
    Model of node row query to acquire from client
    Attributes:
        nodes (Optional[List[NodeQueryIn]]): List of nodes in graph DB
        relations (Optional[List[RelationQueryIn]]): List of relations in graph DB
    """
    nodes: Optional[List[NodeQueryIn]] = []
    relations: Optional[List[RelationQueryIn]] = []


class NodeRowsOut(BaseModel):
    """
    Model of list of rows with nodes
    Attributes:
        rows (Optional[List[List[[BasicNodeOut]]]): List of rows of nodes to return
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list): Hateoas implementation
    """
    rows: Optional[List[List[BasicNodeOut]]] = None
    errors: Optional[Any] = None
    links: Optional[List] = None
