from pydantic import BaseModel
from typing import Optional, Any


class RegisteredChannelIn(BaseModel):
    """
    Model of registered channel to acquire from client

    Attributes:
        channel_id (int): Id of channel
        registered_data_id (id): Id of created registered data

    """
    channel_id: int
    registered_data_id: int


class RegisteredChannelOut(RegisteredChannelIn):
    """
    Model of registered channel to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of activity returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
