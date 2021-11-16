from typing import Optional, Any, List

from models.relation_information_model import RelationInformation
from pydantic import BaseModel


class ParticipationIn(BaseModel):
    """
    Participation model in database

    Attributes:
    activity_execution_id (Optional[int]): Activity execution of participation
    participant_state_id (Optional[int]): Participant state of participation
    """
    activity_execution_id: Optional[int]
    participant_state_id: Optional[int]


class BasicParticipationOut(BaseModel):
    """
    Basic model of participation

    Attributes:
    id (Optional[int]): Id of participation returned from graph api
    """
    id: Optional[int]


class ParticipationOut(BasicParticipationOut):
    """
    Model of participation with relations to send to client as a result of request

    Attributes:
    relations (List[RelationInformation]): List of relations starting in participation node
    reversed_relations (List[RelationInformation]): List of relations ending in participation node
    errors (Optional[Any]): Optional errors appeared during query executions
    links (Optional[list]): List of links available from api
    """
    relations: List[RelationInformation] = []
    reversed_relations: List[RelationInformation] = []
    errors: Optional[Any] = None
    links: Optional[list] = None


class ParticipationsOut(BaseModel):
    """
    Model of participations to send to client as a result of request

    Attributes:
    participations (List[BasicParticipationOut]): Participations from database
    errors (Optional[Any]): Optional errors appeared during query executions
    links (Optional[list]): List of links available from api
    """
    participations: List[BasicParticipationOut] = []
    errors: Optional[Any] = None
    links: Optional[list] = None
