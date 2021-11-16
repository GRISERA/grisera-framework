from pydantic import BaseModel
from typing import Optional, Any


class NotFoundByIdModel(BaseModel):
    """
    Model send when source was not found by id

    Attributes:
        id (int): Id of searching source
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: int = None
    errors: Optional[Any] = None
    links: Optional[list] = None
