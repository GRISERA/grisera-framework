from typing import Union, List

from pydantic import BaseModel

from models.base_model_out import BaseModelOut


class ScenarioIn(BaseModel):
    """
    Model of scenario to acquire from client

    Attributes:
    activity_executions (List[ActivityExecutionIn]): list of activity executions in scenario
    experiment_id (Union[int, str]): Id of experiment
    """

    experiment_id: Union[int, str]
    activity_executions: "List[ActivityExecutionIn]"


class ScenarioOut(ScenarioIn, BaseModelOut):
    """
    Model of scenario to send to client as a result of request

    Attributes:
    activity_executions (List[ActivityExecutionOut]): List of activity executions in scenario
    """

    activity_executions: "List[ActivityExecutionOut]"


class OrderChangeIn(BaseModel):
    """
    Model of ids to change order in scenario

    Attributes:
    previous_id (Union[int, str]): Id of activity execution/experiment to put activity execution after that
    activity_execution_id (Union[int, str]): Id of activity execution to change order of it
    """

    previous_id: Union[int, str]
    activity_execution_id: Union[int, str]


class OrderChangeOut(BaseModelOut):
    """
    Model of changed order in scenario
    """


# circular import exeption prevention
from activity_execution.activity_execution_model import (
    ActivityExecutionIn,
    ActivityExecutionOut,
)

ScenarioIn.update_forward_refs()
ScenarioOut.update_forward_refs()
