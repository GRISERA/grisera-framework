from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum


class FacialHair(str, Enum):
    heavy = "Heavy"
    some = "Some"
    no = "No"


class PersonalityBigFiveIn(BaseModel):
    """
    Model of personality big five model to acquire from client

    Attributes:
        agreeableness (float): Scale of being kind, sympathetic, cooperative, warm, and considerate
        conscientiousness (float): Scale of being neat, and systematic
        extroversion (float): Scale of being outgoing, talkative, energetic
        neuroticism (float): Scale of lack of self-control, poor ability to manage psychological stress
        openess (float): Scale of openness (Intellect) reflects imagination, creativity

    """
    agreeableness: float
    conscientiousness: float
    extroversion: float
    neuroticism: float
    openess: float


class PersonalityBigFiveOut(PersonalityBigFiveIn):
    """
    Model of personality big five model to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of personality big five model returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None


class PersonalityPanasIn(BaseModel):
    """
    Model of personality panas to acquire from client

    Attributes:
        negative_affect (float): Scale of negative affect to community
        positive_affect (float): Scale of positive affect to community
    """
    negative_affect: float
    positive_affect: float


class PersonalityPanasOut(PersonalityPanasIn):
    """
    Model of personality panas to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of personality panas model returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
