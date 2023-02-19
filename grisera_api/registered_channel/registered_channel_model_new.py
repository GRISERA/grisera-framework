from typing import Optional, List, Union

from pydantic import BaseModel

from channel.channel_model_new import ChannelOut
from models.base_model_out import BaseModelOut
from recording.recording_model_new import RecordingOut
from registered_data.registered_data_model_new import RegisteredDataOut


class RegisteredChannelIn(BaseModel):
    """
    Model of registered channel to acquire from client

    Attributes:
    channel_id (Union[int, str]): Channel by which data was registered
    registered_data_id (Union[int, str]): Id of created registered data
    """
    channel_id: Optional[Union[int, str]]
    registered_data_id: Optional[Union[int, str]]


class BasicRegisteredChannelOut(BaseModel):
    """
    Basic model of registered channel

    Attributes:
    id (Optional[Union[int, str]]): Id of registered channel returned from api
    """
    id: Optional[Union[int, str]]


class RegisteredChannelOut(BasicRegisteredChannelOut, BaseModelOut):
    """
    Model of registered channel with relations to send to client as a result of request

    Attributes:
    recordings (Optional[List[RecordingOut]]): recordings related to this registered channel
    channel (Optional[ChannelOut]): channel related to this registered channel
    registeredData (Optional[RegisteredDataOut]): registeredData related to this registered channel
    """
    recordings: Optional[List[RecordingOut]] = []
    channel: Optional[ChannelOut] = []
    registeredData: Optional[RegisteredDataOut] = []


class RegisteredChannelsOut(BaseModelOut):
    """
    Model of registered channels to send to client as a result of request

    Attributes:
    registered_channels (List[BasicRegisteredChannelOut]): Registered channels from database

    """
    registered_channels: List[BasicRegisteredChannelOut] = []
