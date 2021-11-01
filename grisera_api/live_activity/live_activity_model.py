from pydantic import BaseModel
from typing import Optional, Any, List
from enum import Enum
from models.relation_information_model import RelationInformation


class LiveActivity(str, Enum):
    """
    Actions of a human body

    Attributes:
    movement (str): Movement
    sound (str): Sound
    heart_activity (str): Heart activity
    muscles_activity (str): Muscles activity
    perspiration (str): Perspiration
    respiration (str): Respiration
    thermal_regulation (str): Thermal regulation
    brain_activity (str): Brain activity
    """
    movement = "movement"
    sound = "sound"
    heart_activity = "heart activity"
    muscles_activity = "muscles activity"
    perspiration = "perspiration"
    respiration = "respiration"
    thermal_regulation = "thermal regulation"
    brain_activity = "brain activity"


class LiveActivityIn(BaseModel):
    """
    Model of actions of a human body observed during experiment

    Attributes:
    live_activity (str): Actions of a human body
    """
    live_activity: str


class BasicLiveActivityOut(LiveActivityIn):
    """
    Model of actions of a human body during experiment in database

    Attributes:
    id (Optional[int]): Id of node returned from graph api
    """
    id: Optional[int]


class LiveActivityOut(BasicLiveActivityOut):
    """
    Model of actions of a human body during experiment to send to client as a result of request

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


class LiveActivitiesOut(BaseModel):
    """
    Model of actions of a human body during experiment to send to client as a result of request

    Attributes:
    live_activities (List[BasicLiveActivityOut]): Live activities from database
    errors (Optional[Any]): Optional errors appeared during query executions
    links (Optional[list]): List of links available from api
    """
    live_activities: List[BasicLiveActivityOut] = []
    errors: Optional[Any] = None
    links: Optional[list] = None
