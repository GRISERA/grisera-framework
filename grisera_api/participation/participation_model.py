from pydantic import BaseModel
from typing import Optional, Any


class ParticipationIn(BaseModel):
    """
    Participation model in database

    Attributes:
        activity_id (Optional[int]): Activity of participation
        participant_state_id (Optional[int]): Participant of participation
    """
    activity_id: Optional[int]
    participant_state_id: Optional[int]


class ParticipationOut(ParticipationIn):
    """
    Model of participation to send to client

    Attributes:
        id (Optional[int]): Id of participation node in database
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None

