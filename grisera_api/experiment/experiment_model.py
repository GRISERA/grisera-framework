from pydantic import BaseModel
from typing import Optional, Any


class ExperimentIn(BaseModel):
    """
    Model of experiment to acquire from client

    Attributes:
        name (str): Name of experiment
    """
    name: str


class ExperimentOut(ExperimentIn):
    """
    Model of experiment to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of experiment returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
