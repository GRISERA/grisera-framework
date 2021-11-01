from pydantic import BaseModel
from typing import Optional, Any, List, Union
from enum import Enum
from models.relation_information_model import RelationInformation


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


class BasicPersonalityBigFiveOut(PersonalityBigFiveIn):
    """
    Basic model of personality big five model to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of personality big five model returned from graph api
    """
    id: Optional[int]


class PersonalityBigFiveOut(BasicPersonalityBigFiveOut):
    """
    Model of personality big five model with relationships to send to client as a result of request

    Attributes:
        relations (List[RelationInformation]): List of relations starting in personality node
        reversed_relations (List[RelationInformation]): List of relations ending in personality node
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    relations: List[RelationInformation] = []
    reversed_relations: List[RelationInformation] = []
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


class BasicPersonalityPanasOut(PersonalityPanasIn):
    """
    Basic model of personality panas to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of personality panas returned from graph api
    """
    id: Optional[int]


class PersonalityPanasOut(BasicPersonalityPanasOut):
    """
    Model of personality panas with relationships to send to client as a result of request

    Attributes:
        relations (List[RelationInformation]): List of relations starting in personality node
        reversed_relations (List[RelationInformation]): List of relations ending in personality node
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    relations: List[RelationInformation] = []
    reversed_relations: List[RelationInformation] = []
    errors: Optional[Any] = None
    links: Optional[list] = None


class PersonalitiesOut(BaseModel):
    """
    Model of personalities to send to client as a result of request

    Attributes:
        personalities (List[Union[BasicPersonalityBigFiveOut, BasicPersonalityPanasOut]]): Personalities from database
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    personalities: List[Union[BasicPersonalityBigFiveOut, BasicPersonalityPanasOut]] = []
    errors: Optional[Any] = None
    links: Optional[list] = None
