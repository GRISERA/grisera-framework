from typing import List
from pydantic import BaseModel
from typing import Optional, Any
from activity_execution.activity_execution_model import ActivityExecutionIn, ActivityExecutionOut


class ScenarioIn(BaseModel):
    """
    Model of scenario to acquire from client

    Attributes:
        activity_executions (List[ActivityExecutionIn]): list of activity executions in scenario
        experiment_id (int): Id of experiment
    """
    experiment_id: int
    activity_executions: List[ActivityExecutionIn]


class ScenarioOut(ScenarioIn):
    """
    Model of scenario to send to client as a result of request

    Attributes:
        activity_executions (List[ActivityExecutionOut]): List of activity executions in scenario
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    activity_executions: List[ActivityExecutionOut]
    errors: Optional[Any] = None
    links: Optional[list] = None


class OrderChangeIn(BaseModel):
    """
    Model of ids to change order in scenario

    Attributes:
        previous_id (int): Id of activity execution/experiment to put activity execution after that
        activity_execution_id (int): Id of activity execution to change order of it
    """
    previous_id: int
    activity_execution_id: int


class OrderChangeOut(OrderChangeIn):
    """
    Model of changed order in scenario

    Attributes:
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    errors: Optional[Any] = None
    links: Optional[list] = None
