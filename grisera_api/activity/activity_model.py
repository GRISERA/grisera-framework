from typing import Optional, Union, List
from enum import Enum

from pydantic import BaseModel

from activity_execution.activity_execution_model import ActivityExecutionOut
from models.base_model_out import BaseModelOut
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
    id (Optional[Union[int, str]]): identity of activity returned from api
    """

    id: Optional[Union[int, str]]


class ActivityOut(BasicActivityOut, BaseModelOut):
    """
    Model of activity to send to client as a result of request

    Attributes:
    activity_executions (Optional[ActivityExecutionOut]): activity_executions related to this activity
    """

    activity_executions: Optional[List[ActivityExecutionOut]]


class ActivitiesOut(BaseModelOut):
    """
    Model of activities to send to client as a result of request

    Attributes:
    activity_types (List[BasicActivityOut]): Activity types from database
    """

    activities: List[BasicActivityOut] = []
