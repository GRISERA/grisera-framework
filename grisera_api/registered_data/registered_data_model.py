from typing import List
from pydantic import BaseModel
from typing import Optional, Any
from property.property_model import PropertyIn


class RegisteredDataIn(BaseModel):
    """
    Model of registered data to acquire from client

    Attributes:
        source (str): URI address where recorded data is located

    """
    source: str
    additional_properties: Optional[List[PropertyIn]]


class RegisteredDataOut(RegisteredDataIn):
    """
    Model of registered data to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of activity returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
