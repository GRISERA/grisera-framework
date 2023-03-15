from typing import Optional, List, Union

from pydantic import BaseModel

from ..models.base_model_out import BaseModelOut
from ..activity_execution.activity_execution_model import ActivityExecutionOut
from ..participant_state.participant_state_model import ParticipantStateOut
from ..recording.recording_model import RecordingOut


class ParticipationIn(BaseModel):
    """
    Participation model in database

    Attributes:
    activity_execution_id (Optional[int]): Activity execution of participation
    participant_state_id (Optional[int]): Participant state of participation
    """

    activity_execution_id: Optional[Union[int, str]]
    participant_state_id: Optional[Union[int, str]]


class BasicParticipationOut(BaseModel):
    """
    Basic model of participation

    Attributes:
    id (Optional[Union[int, str]]): Id of participation returned from api
    """

    id: Optional[Union[int, str]]


class ParticipationOut(BasicParticipationOut, BaseModelOut):
    """
    Model of participation with relations to send to client as a result of request

    Attributes:
    participant_state (Optional[List[ParticipantStateOut]]): participant state related to this participation
    activity_execution (Optional[List[ActivityExecutionOut]]): activity execution related to this participation
    recordings (Optional[List[RecordingOut]]): recordings related to this participation
    """

    participant_state: Optional[ParticipantStateOut]
    activity_execution: Optional[ActivityExecutionOut]
    recordings: Optional[List[RecordingOut]]


class ParticipationsOut(BaseModelOut):
    """
    Model of participations to send to client as a result of request

    Attributes:
    participations (List[BasicParticipationOut]): Participations from database
    """

    participations: List[BasicParticipationOut] = []
