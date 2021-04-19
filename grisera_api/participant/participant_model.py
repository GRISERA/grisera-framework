from typing import List
from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum
from property.property_model import PropertyIn


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


class ParticipantIn(BaseModel):
    """
    Model of participant to acquire from client

    Attributes:
        age (Optional[int]): Age of participant
        sex (Optional[Sex]): Sex of participant
        beard (Optional[FacialHair]): Type of participant's beard
        moustache (Optional[FacialHair]): Type of participant's moustache
        glasses (Optional[bool]): Did participant have glasses
        disorder (Optional[bool]): Was participant disordered
        disorder_type (Optional[str]): Type of disorder
        additional_properties (Optional[List[PropertyIn]]): Additional properties for participant
    """
    age: Optional[int]
    sex: Optional[Sex]
    beard: Optional[FacialHair]
    moustache: Optional[FacialHair]
    glasses: Optional[bool]
    disorder: Optional[bool]
    disorder_type: Optional[str]
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
