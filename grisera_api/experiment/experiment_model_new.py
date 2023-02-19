from typing import Optional, Union, List

from pydantic import BaseModel

from activity_execution.activity_execution_model_new import ActivityExecutionOut
from property.property_model import PropertyIn
from models.base_model_out import BaseModelOut


class ExperimentIn(BaseModel):
    """
    Model of experiment to acquire from client

    Attributes:
    experiment_name (str): Name of experiment
    additional_properties (Optional[List[PropertyIn]]): Additional properties for experiment
    """
    experiment_name: str
    additional_properties: Optional[List[PropertyIn]]


class BasicExperimentOut(ExperimentIn):
    """
    Basic model of experiment to send to client as a result of request

    Attributes:
    id (Union[int, str]): Id of experiment returned from api
    """
    id: Optional[Union[int, str]]


class ExperimentOut(BasicExperimentOut, BaseModelOut):
    """
    Model of experiment with relationships to send to client as a result of request

    Attributes:
    activity_executions (Optional[ActivityExecutionOut]): activity_executions related to this experiment
    """
    activity_executions: Optional[ActivityExecutionOut] = []


class ExperimentsOut(BaseModelOut):
    """
    Model of experiments to send to client as a result of request

    Attributes:
    experiments (List[BasicExperimentOut]): Experiments from database
    """
    experiments: List[BasicExperimentOut] = []
