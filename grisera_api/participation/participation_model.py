from pydantic import BaseModel
from typing import Optional, Any


class ParticipationIn(BaseModel):
    """
    Model of participation to acquire from client

    Attributes:
    """


class ParticipationOut(ParticipationIn):
    """
    Model of participation to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of participation returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
