from typing import Optional, Any
from pydantic import BaseModel


class ModelOut(BaseModel):
    """
    Model of model to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of model returned from notology database
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list): Hateoas implementation
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
