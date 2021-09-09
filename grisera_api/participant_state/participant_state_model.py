from typing import List
from pydantic import BaseModel
from typing import Optional, Any
from property.property_model import PropertyIn
from participant.participant_model import ParticipantIn, ParticipantOut


class ParticipantStateIn(BaseModel):
    """
    Model of participant state to acquire from client

    Attributes:
        participant (Optional[ParticipantIn]): Participant whose state is described
        age (Optional[int]): Age of participant state
        personality_id (Optional[int]): Id of personality describing participant
        appearance_id (Optional[int]): Id of appearance describing participant
        additional_properties (Optional[List[PropertyIn]]): Additional properties for participant state
    """
    participant: Optional[ParticipantIn]
    age: Optional[int]
    personality_id: Optional[int] = None
    appearance_id: Optional[int] = None
    additional_properties: Optional[List[PropertyIn]]


class ParticipantStateOut(ParticipantStateIn):
    """
    Model of participant state to send to client as a result of request

    Attributes:
        participant (Optional[ParticipantOut]): Participant whose state is described
        id (Optional[int]): Id of participant state returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    participant: Optional[ParticipantOut]
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
