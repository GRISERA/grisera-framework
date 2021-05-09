from typing import List
from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum
from property.property_model import PropertyIn


class Type(str, Enum):
    """
    The type of activity

    Attributes:
        individual (str): Individual activity
        two_people (str): Two people activity
        group (str): Group activity
    """
    individual = "individual"
    two_people = "two-people"
    group = "group"


class ActivityIn(BaseModel):
    """
    Model of activity to acquire from client

    Attributes:
        identifier (int): Activity identifier
        name (Optional[str]: Name of the activity
        type (Optional[Type]): Type of the activity
        layout (Optional[str]): The placement of participants
        additional_properties (Optional[List[PropertyIn]]): Additional properties for activity
    """
    identifier: int
    name: Optional[str]
    type: Optional[Type]
    layout: Optional[str]
    additional_properties: Optional[List[PropertyIn]]


class ActivityOut(ActivityIn):
    """
    Model of activity to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of activity returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
