from typing import Optional, Any, List

from models.relation_information_model import RelationInformation
from pydantic import BaseModel


class RegisteredChannelIn(BaseModel):
    """
    Model of registered channel to acquire from client

    Attributes:
    channel_id (int): Channel by which data was registered
    registered_data_id (int): Id of created registered data
    """
    channel_id: Optional[int]
    registered_data_id: Optional[int]


class BasicRegisteredChannelOut(BaseModel):
    """
    Basic model of registered channel

    Attributes:
    id (Optional[int]): Id of registered channel returned from graph api
    """
    id: Optional[int]


class RegisteredChannelOut(BasicRegisteredChannelOut):
    """
    Model of registered channel with relations to send to client as a result of request

    Attributes:
    relations (List[RelationInformation]): List of relations starting in registered channel node
    reversed_relations (List[RelationInformation]): List of relations ending in registered channel node
    errors (Optional[Any]): Optional errors appeared during query executions
    links (Optional[list]): List of links available from api
    """
    relations: List[RelationInformation] = []
    reversed_relations: List[RelationInformation] = []
    errors: Optional[Any] = None
    links: Optional[list] = None


class RegisteredChannelsOut(BaseModel):
    """
    Model of registered channels to send to client as a result of request

    Attributes:
    registered_channels (List[BasicRegisteredChannelOut]): Registered channels from database
    errors (Optional[Any]): Optional errors appeared during query executions
    links (Optional[list]): List of links available from api
    """
    registered_channels: List[BasicRegisteredChannelOut] = []
    errors: Optional[Any] = None
    links: Optional[list] = None
