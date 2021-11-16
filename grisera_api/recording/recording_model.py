from typing import Optional, Any, List

from models.relation_information_model import RelationInformation
from property.property_model import PropertyIn
from pydantic import BaseModel


class RecordingPropertyIn(BaseModel):
    """
    Model of recording to acquire from client

    Attributes:
    additional_properties (Optional[List[PropertyIn]]): Additional properties for recording
    """
    additional_properties: Optional[List[PropertyIn]]


class RecordingRelationIn(BaseModel):
    """
    Model of recording relations to acquire from client

    Attributes:
    participation_id (Optional[int]) : id of participation
    registered_channel_id (Optional[int]): id of registered channel
    """
    participation_id: Optional[int]
    registered_channel_id: Optional[int]


class RecordingIn(RecordingPropertyIn, RecordingRelationIn):
    """
    Full model of recording to acquire from client

    """


class BasicRecordingOut(RecordingIn):
    """
    Basic Model of recording

    Attributes:
    id (Optional[int]): Id of recording returned from graph api
    """
    id: Optional[int]


class RecordingOut(BasicRecordingOut):
    """
    Model of recording with relations to send to client as a result of request

    Attributes:

    relations (List[RelationInformation]): List of relations starting in recording node
    reversed_relations (List[RelationInformation]): List of relations ending in recording node
    errors (Optional[Any]): Optional errors appeared during query executions
    links (Optional[list]): List of links available from api
    """
    relations: List[RelationInformation] = []
    reversed_relations: List[RelationInformation] = []
    errors: Optional[Any] = None
    links: Optional[list] = None


class RecordingsOut(BasicRecordingOut):
    """
    Model of recordings to send to client as a result of request

    Attributes:
    recordings (List[BasicRecordingOut]): Recordings from database
    errors (Optional[Any]): Optional errors appeared during query executions
    links (Optional[list]): List of links available from api
    """
    recordings: List[BasicRecordingOut] = []
    errors: Optional[Any] = None
    links: Optional[list] = None
