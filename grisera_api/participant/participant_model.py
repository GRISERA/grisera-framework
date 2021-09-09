from typing import List
from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum
from property.property_model import PropertyIn
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


class ParticipantOut(ParticipantIn):
    """
    Model of participant to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of participant returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
