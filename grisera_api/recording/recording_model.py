from typing import Optional, Any
from pydantic import BaseModel


class RecordingIn(BaseModel):
    """
    Model of recording to acquire from client

    Attributes:
        participation_id (Optional[int]) : id of participation
        registered_channel_id (Optional[int]): id of registered channel
    """
    participation_id: Optional[int]
    registered_channel_id: Optional[int]


class RecordingOut(RecordingIn):
    """
    Model of recording to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of recording returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
