from typing import List
from pydantic import BaseModel
from typing import Optional, Any
from activity.activity_model import ActivityIn, ActivityOut


class ScenarioIn(BaseModel):
    """
    Model of scenario to acquire from client

    Attributes:
        activities (List[ActivityIn]): list of activities in scenario
        experiment_id (int): Id of experiment
    """
    experiment_id: int
    activities: List[ActivityIn]


class ScenarioOut(ScenarioIn):
    """
    Model of scenario to send to client as a result of request

    Attributes:
        activities (List[ActivityOut]): List of activities in scenario
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    activities: List[ActivityOut]
    errors: Optional[Any] = None
    links: Optional[list] = None


class OrderChangeIn(BaseModel):
    """
    Model of ids to change order in scenario

    Attributes:
        previous_id (int): Id of activity/experiment to put activity after that
        activity_id (int): Id of activity to change order of it
    """
    previous_id: int
    activity_id: int


class OrderChangeOut(OrderChangeIn):
    """
    Model of changed order in scenario

    Attributes:
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    errors: Optional[Any] = None
    links: Optional[list] = None
