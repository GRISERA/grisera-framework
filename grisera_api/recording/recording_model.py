from pydantic import BaseModel
from typing import Optional, Any, List


class RecordingIn(BaseModel):
    """
    Recording model in database

    Attributes:
        activity_id (Optional[int]): Activity of recording
        participant_state_id (Optional[int]): Participant of recording
    """
    activity_id: Optional[int]
    participant_state_id: Optional[int]


class RecordingOut(RecordingIn):
    """
    Model of recording to send to client

    Attributes:
        id (Optional[int]): Id of recording node in database
        errors (Optional[Any]): Optional errors appeared during query executions
    """
    id: Optional[int]
    errors: Optional[Any] = None


class RecordingsIn(BaseModel):
    """
    Model of recordings to acquire from client

    Attributes:
        activities (List[int]): List of activities participated
        participant_state_id (Optional[int]): Participant of activities
        experiment_id (Optional[int]): Experiment
    """
    activities: List[int]
    participant_state_id: Optional[int]
    experiment_id: Optional[int]


class RecordingsOut(BaseModel):
    """
    Model of recordings to send to client as a result of request

    Attributes:
        recordings (List[RecordingOut]): Created recording nodes
        links (Optional[list]): List of links available from api
    """
    recordings: List[RecordingOut] = None
    links: Optional[list] = None
