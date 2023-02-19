from typing import Optional, List, Union

from pydantic import BaseModel

from participation.participation_model_new import ParticipationOut
from property.property_model import PropertyIn
from activity.activity_model_new import ActivityOut
from experiment.experiment_model_new import ExperimentOut
from models.base_model_out import BaseModelOut


class ActivityExecutionPropertyIn(BaseModel):
    """
    Model of activity execution to acquire from client

    Attributes:
    additional_properties (Optional[List[PropertyIn]]): Additional properties for activity execution
    """
    additional_properties: Optional[List[PropertyIn]]


class ActivityExecutionRelationIn(BaseModel):
    """
    Model of activity execution relations to acquire from client

    Attributes:
    activity_id (int): Id of activity
    arrangement_id (int) : Id of arrangement
    """
    activity_id: Optional[Union[int, str]]
    arrangement_id: Optional[Union[int, str]]


class ActivityExecutionIn(ActivityExecutionPropertyIn, ActivityExecutionRelationIn):
    """
    Full model of activity execution to acquire from client

    """


class BasicActivityExecutionOut(ActivityExecutionPropertyIn):
    """
    Basic model of activity execution

    Attributes:
    id (Optional[Union[int, str]]): Id of activity execution returned from api
    """
    id: Optional[Union[int, str]]


class ActivityExecutionOut(BasicActivityExecutionOut, BaseModelOut):
    """
    Model of activity execution to send to client as a result of request

    Attributes:
    activity (Optional[ActivityOut]): activity related to this activity execution
    participations (Optional[List[ParticipationOut]]): participations related to this activity execution
    experiments (Optional[List[ExperimentOut]]): experiments related to this participation
    """
    activity: Optional[ActivityOut] = None
    participations: Optional[List[ParticipationOut]] = None
    experiments: Optional[List[ExperimentOut]] = None


class ActivityExecutionsOut(BaseModelOut):
    """
    Model of activity executions to send to client as a result of request

    Attributes:
    activity_executions (List[BasicActivityExecutionOut]): Activity executions from database
    """
    activity_executions: List[BasicActivityExecutionOut] = []
