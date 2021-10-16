from typing import List
from pydantic import BaseModel
from typing import Optional, Any
from property.property_model import PropertyIn
from models.relation_information_model import RelationInformation


class ParticipantStateIn(BaseModel):
    """
    Model of participant state to acquire from client

    Attributes:
        age (Optional[int]): Age of participant state
        additional_properties (Optional[List[PropertyIn]]): Additional properties for participant state
    """
    age: Optional[int]
    additional_properties: Optional[List[PropertyIn]]


class ParticipantStateRelationIn(ParticipantStateIn):
    """
    Model of participant state with relations to acquire from client

    Attributes:
        participant_id (Optional[int]): Participant whose state is described
        personality_id (Optional[int]): Id of personality describing participant
        appearance_id (Optional[int]): Id of appearance describing participant
    """
    participant_id: Optional[int]
    personality_id: Optional[int] = None
    appearance_id: Optional[int] = None


class BasicParticipantStateRelationOut(ParticipantStateRelationIn):
    """
    Basic model of participant state with relations

    Attributes:
        id (Optional[int]): Id of participant returned from graph api
    """
    id: Optional[int]


class BasicParticipantStateOut(ParticipantStateIn):
    """
    Basic model of participant

    Attributes:
        id (Optional[int]): Id of participant returned from graph api
    """
    id: Optional[int]


class ParticipantStateOut(BasicParticipantStateRelationOut):
    """
    Model of participant state to send to client as a result of request

    Attributes:
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    errors: Optional[Any] = None
    links: Optional[list] = None


class ParticipantStateRelationOut(BasicParticipantStateOut):
    """
    Model of participant state with relations to send to client as a result of request

    Attributes:
        relations (List[RelationInformation]): List of relations starting in participant state node
        reversed_relations (List[RelationInformation]): List of relations ending in participant state node
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    relations: List[RelationInformation] = []
    reversed_relations: List[RelationInformation] = []
    errors: Optional[Any] = None
    links: Optional[list] = None


class ParticipantStatesOut(BaseModel):
    """
    Model of participant states to send to client as a result of request

    Attributes:
        participant_states (List[BasicParticipantStateOut]): Participant states from database
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    participant_states: List[BasicParticipantStateOut] = []
    errors: Optional[Any] = None
    links: Optional[list] = None
