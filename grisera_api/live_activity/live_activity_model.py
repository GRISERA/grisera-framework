from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum


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
        live_activity (LiveActivity): Actions of a human body
    """
    live_activity: LiveActivity


class LiveActivityOut(LiveActivityIn):
    """
    Model of actions of a human body during experiment to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of node returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
