from typing import Optional, List, Union

from pydantic import BaseModel

from models.base_model_out import BaseModelOut
from property.property_model import PropertyIn


class RecordingPropertyIn(BaseModel):
    """
    Model of recording to acquire from client

    Attributes:
    additional_properties (Optional[List[PropertyIn]]): Additional properties for recording
    """

    additional_properties: Optional[List[PropertyIn]]


class RecordingRelationIn(BaseModel):
    """
    Model of recording relations to acquire from client

    Attributes:
    participation_id (Optional[Union[int, str]]) : id of participation
    registered_channel_id (Optional[Union[int, str]]): id of registered channel
    """

    participation_id: Optional[Union[int, str]]
    registered_channel_id: Optional[Union[int, str]]


class RecordingIn(RecordingPropertyIn, RecordingRelationIn):
    """
    Full model of recording to acquire from client

    """


class BasicRecordingOut(RecordingIn,BaseModelOut):
    """
    Basic Model of recording

    Attributes:
    id (Optional[Union[int, str]]): Id of recording returned from api
    """

    id: Optional[Union[int, str]]


class RecordingOut(BasicRecordingOut, BaseModelOut):
    """
    Model of recording with relations to send to client as a result of request

    Attributes:
    registered_channel (Optional[RegisteredChannelOut]): registered channel related to this recording
    participation (Optional[ParticipationOut]): participation related to this recording
    observable_informations (Optional[List[ObservableInformationOut]]): List of observable informations related to
        this recording
    """

    registered_channel: "Optional[RegisteredChannelOut]"
    participation: "Optional[ParticipationOut]"
    observable_informations: "Optional[List[ObservableInformationOut]]"


class RecordingsOut(BaseModelOut):
    """
    Model of recordings to send to client as a result of request

    Attributes:
    recordings (List[BasicRecordingOut]): Recordings from database
    """

    recordings: List[BasicRecordingOut] = []


# Circular import exception prevention
from observable_information.observable_information_model import ObservableInformationOut
from participation.participation_model import ParticipationOut
from registered_channel.registered_channel_model import RegisteredChannelOut

RecordingOut.update_forward_refs()
