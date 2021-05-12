from typing import List
from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum
from property.property_model import PropertyIn
from participant.participant_model import ParticipantIn


class FacialHair(str, Enum):
    """
    Types of facial hair

    Attributes:
        heavy (str): Heavy facial hair
        no (str): No facial hair
        some (str): Some facial hair
    """
    heavy = "heavy"
    no = "no"
    some = "some"


class ParticipantStateIn(BaseModel):
    """
    Model of participant state to acquire from client

    Attributes:
        age (Optional[int]): Age of participant state
        beard (Optional[FacialHair]): Type of participant state's beard
        moustache (Optional[FacialHair]): Type of participant state's moustache
        glasses (Optional[bool]): Did participant state have glasses
        additional_properties (Optional[List[PropertyIn]]): Additional properties for participant state
    """
    participant: Optional[ParticipantIn]
    age: Optional[int]
    beard: Optional[FacialHair]
    moustache: Optional[FacialHair]
    glasses: Optional[bool]
    additional_properties: Optional[List[PropertyIn]]


class ParticipantStateOut(ParticipantStateIn):
    """
    Model of participant state to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of participant state returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
