from pydantic import BaseModel
from typing import Optional, Any, List


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
    """
    id: Optional[int]
    errors: Optional[Any] = None


class ParticipationsIn(BaseModel):
    """
    Model of participations to acquire from client

    Attributes:
        activities (List[int]): List of activities participated
        participant_state_id (Optional[int]): Participant of activities
        experiment_id (Optional[int]): Experiment
    """
    activities: List[int]
    participant_state_id: Optional[int]
    experiment_id: Optional[int]


class ParticipationsOut(BaseModel):
    """
    Model of participations to send to client as a result of request

    Attributes:
        participations (List[ParticipationOut]): Created participation nodes
        links (Optional[list]): List of links available from api
    """
    participations: List[ParticipationOut] = None
    links: Optional[list] = None
