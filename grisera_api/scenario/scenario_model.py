from typing import List
from pydantic import BaseModel
from typing import Optional, Any
from activity.activity_model import ActivityIn


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
        id (Optional[int]): Id of scenario returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
