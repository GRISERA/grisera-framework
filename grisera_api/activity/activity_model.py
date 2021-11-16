from pydantic import BaseModel
from typing import Optional, Any, List
from enum import Enum
from models.relation_information_model import RelationInformation
from property.property_model import PropertyIn


class Activity(str, Enum):
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
    Model of activity

    Attributes:
    activity (str): Type of activity
    additional_properties (Optional[List[PropertyIn]]): Additional properties for activity
    """
    activity: str
    additional_properties: Optional[List[PropertyIn]]


class BasicActivityOut(ActivityIn):
    """
    Model of activity in database

    Attributes:
    id (Optional[int]): Id of activity returned from graph api
    """
    id: Optional[int]


class ActivityOut(BasicActivityOut):
    """
    Model of activity to send to client as a result of request

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


class ActivitiesOut(BaseModel):
    """
    Model of activities to send to client as a result of request

    Attributes:
    activity_types (List[BasicActivityOut]): Activity types from database
    errors (Optional[Any]): Optional errors appeared during query executions
    links (Optional[list]): List of links available from api
    """
    activities: List[BasicActivityOut] = []
    errors: Optional[Any] = None
    links: Optional[list] = None
