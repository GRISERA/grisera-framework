from typing import List
from pydantic import BaseModel
from typing import Optional, Any
from property.property_model import PropertyIn


class ActivityExecutionIn(BaseModel):
    """
    Model of activity_execution to acquire from client

    Attributes:
        activity (str): Type of the activity execution
        identifier (int): ActivityExecution identifier
        name (Optional[str]: Name of the activity execution
        layout (Optional[str]): The placement of participants
        additional_properties (Optional[List[PropertyIn]]): Additional properties for activity execution
    """
    activity: str
    identifier: int
    name: Optional[str]
    layout: Optional[str]
    additional_properties: Optional[List[PropertyIn]]


class ActivityExecutionOut(ActivityExecutionIn):
    """
    Model of activity execution to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of activity execution returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
