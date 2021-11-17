from typing import List
from pydantic import BaseModel
from typing import Optional, Any
from property.property_model import PropertyIn
from models.relation_information_model import RelationInformation


class RegisteredDataIn(BaseModel):
    """
    Model of registered data to acquire from client

    Attributes:
    source (str): URI address where recorded data is located

    """
    source: str
    additional_properties: Optional[List[PropertyIn]]


class BasicRegisteredDataOut(RegisteredDataIn):
    """
    Basic model of registered data to send to client as a result of request

    Attributes:
    id (Optional[int]): Id of registered data returned from graph api
    """
    id: Optional[int]


class RegisteredDataOut(BasicRegisteredDataOut):
    """
    Model of registered data with relationships to send to client as a result of request

    Attributes:
    relations (List[RelationInformation]): List of relations starting in registered data node
    reversed_relations (List[RelationInformation]): List of relations ending in registered data node
    errors (Optional[Any]): Optional errors appeared during query executions
    links (Optional[list]): List of links available from api
    """
    relations: List[RelationInformation] = []
    reversed_relations: List[RelationInformation] = []
    errors: Optional[Any] = None
    links: Optional[list] = None


class RegisteredDataNodesOut(BaseModel):
    """
    Model of registered data nodes to send to client as a result of request

    Attributes:
    registered_data_nodes (List[BasicRegisteredDataOut]): Registered Data nodes from database
    errors (Optional[Any]): Optional errors appeared during query executions
    links (Optional[list]): List of links available from api
    """
    registered_data_nodes: List[BasicRegisteredDataOut] = []
    errors: Optional[Any] = None
    links: Optional[list] = None
