from typing import List
from typing import Optional, Union

from pydantic import BaseModel

from appearance.appearance_model import (
    AppearanceSomatotypeOut,
    AppearanceOcclusionOut,
)
from participation.participation_model import ParticipationOut
from participant.participant_model import ParticipantOut
from personality.personality_model import PersonalityBigFiveOut, PersonalityPanasOut
from property.property_model import PropertyIn
from models.base_model_out import BaseModelOut


class ParticipantStatePropertyIn(BaseModel):
    """
    Model of participant state to acquire from client

    Attributes:
        age (Optional[int]): Age of participant state
        additional_properties (Optional[List[PropertyIn]]): Additional properties for participant state
    """

    age: Optional[int]
    additional_properties: Optional[List[PropertyIn]]


class ParticipantStateRelationIn(BaseModel):
    """
    Model of participant state relations to acquire from client

    Attributes:
        participant_id (Optional[int]): Participant whose state is described
        personality_id (Optional[int]): Id of personality describing participant
        appearance_id (Optional[int]): Id of appearance describing participant
    """

    participant_id: Optional[Union[int, str]] = None
    personality_id: Optional[Union[int, str]] = None
    appearance_id: Optional[Union[int, str]] = None


class ParticipantStateIn(ParticipantStatePropertyIn, ParticipantStateRelationIn):
    """
    Full model of participant state to acquire from client
    """


class BasicParticipantStateOut(ParticipantStatePropertyIn):
    """
    Basic model of participant

    Attributes:
        id (Optional[int]): Id of participant returned from api
    """

    id: Optional[Union[int, str]]


class ParticipantStateOut(BasicParticipantStateOut, BaseModelOut):
    """
    Model of participant state with optional related fields to send to client as a result of request

    Attributes:
        participations (Optional[List[BasicParticipationOut]]): participations with this participant state
        participant (Optional[BasicParticipantOut]): participant related to this participant state
        appearance (Optional[Union[BasicAppearanceSomatotypeOut, BasicAppearanceOcclusionOut]]): appearance related to
            this participant state
        personality (Optional[Union[BasicPersonalityBigFiveOut, BasicPersonalityPanasOut]]): personality related to this
            participant state
    """

    participations: Optional[List[ParticipationOut]]
    participant: Optional[ParticipantOut]
    appearance: Optional[Union[AppearanceSomatotypeOut, AppearanceOcclusionOut]]
    personality: Optional[Union[PersonalityBigFiveOut, PersonalityPanasOut]]


class ParticipantStatesOut(BaseModelOut):
    """
    Model of participant states to send to client as a result of request

    Attributes:
        participant_states (List[BasicParticipantStateOut]): Participant states from database
    """

    participant_states: List[BasicParticipantStateOut] = []
