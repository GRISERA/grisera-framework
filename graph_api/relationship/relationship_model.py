from typing import Set, Optional, Any
from pydantic import BaseModel


class RelationshipIn(BaseModel):
    """
        Model of relationship to acquire from client

        Attributes:
            start_node (int): Id of node which starts connection
            end_node (int): Id of node which ends connection
            name (str): Name of the relationship
    """

    start_node: int
    end_node: int
    name: str


class RelationshipOut(RelationshipIn):
    """
        Model of relationship to send to client as a result of request

        Attributes:
            id (Optional[int]): Id of relationship returned from graph database
            errors (Optional[Any]): Optional errors appeared during query executions
    """

    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
