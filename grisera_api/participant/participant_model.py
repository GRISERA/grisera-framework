from typing import List
from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum
from property.property_model import PropertyIn
from models.relation_information_model import RelationInformation
from datetime import date


class Sex(str, Enum):
    """
    The sexes

    Attributes:
        male (str): Male sex
        female (str): Female sex
        not_given (str): Sex was not given
    """
    male = "male"
    female = "female"
    not_given = "not given"


class ParticipantIn(BaseModel):
    """
    Model of participant to acquire from client

    Attributes:
        name (str): Name of the participant
        date_of_birth (Optional[date]): Date of birth of participant
        sex (Optional[Sex]): Sex of participant
        disorder (Optional[str]): Type of disorder
        additional_properties (Optional[List[PropertyIn]]): Additional properties for participant
    """
    name: str
    date_of_birth: Optional[date]
    sex: Optional[Sex]
    disorder: Optional[str]
    additional_properties: Optional[List[PropertyIn]]


class BasicParticipantOut(ParticipantIn):
    """
    Basic model of participant to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of participant returned from graph api
    """
    id: Optional[int]


class ParticipantOut(BasicParticipantOut):
    """
    Model of participant with relationships to send to client as a result of request

    Attributes:
        relations (List[RelationInformation]): List of relations starting in participant node
        reversed_relations (List[RelationInformation]): List of relations ending in participant node
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    relations: List[RelationInformation] = []
    reversed_relations: List[RelationInformation] = []
    errors: Optional[Any] = None
    links: Optional[list] = None


class ParticipantsOut(BaseModel):
    """
    Model of participants to send to client as a result of request

    Attributes:
        participants (List[BasicParticipantOut]): Participants from database
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    participants: List[BasicParticipantOut] = []
    errors: Optional[Any] = None
    links: Optional[list] = None
