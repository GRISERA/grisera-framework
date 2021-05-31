from pydantic import BaseModel
from typing import Optional, Any


class ChannelIn(BaseModel):
    """
    Model of channel

    Attributes:
        type (str): Type of the channel
    """
    type: str


class ChannelOut(ChannelIn):
    """
    Model of channel to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of channel returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
