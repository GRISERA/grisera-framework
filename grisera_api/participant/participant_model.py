from pydantic import BaseModel
from typing import Optional, Any


class ParticipantIn(BaseModel):
    """
    Model of participant to acquire from client
    """


class ParticipantOut(ParticipantIn):
    """
    Model of participant to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of participant returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
