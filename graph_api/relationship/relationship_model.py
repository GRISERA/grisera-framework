from typing import Optional, Any, List
from pydantic import BaseModel
from property.property_model import PropertyIn


class RelationshipIn(BaseModel):
    """
        Model of relationship to acquire from client

        Attributes:
            start_node (Optional[int]): Id of node which starts connection
            end_node (Optional[int]): Id of node which ends connection
            name (Optional[str]): Name of the relationship
    """

    start_node: int = None
    end_node: int = None
    name: str = None


class RelationshipOut(RelationshipIn):
    """
        Model of relationship to send to client as a result of request

        Attributes:
            id (Optional[int]): Id of relationship returned from graph database
            propeties(Optional[List[PropertyIn]]): List of properties of the relationship in the database
            errors (Optional[Any]): Optional errors appeared during query executions
    """

    id: Optional[int] = None
    properties: Optional[List[PropertyIn]] = None
    errors: Optional[Any] = None
    links: Optional[list] = None
