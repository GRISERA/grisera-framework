from pydantic import BaseModel
from typing import Optional, Any


class MeasureIn(BaseModel):
    """
    Model of measure to acquire from client

    Attributes:
        measure_name (str): Name of the measure
        data_type (str): Type of data
        range (str): Range of measure
    """
    measure_name: str
    data_type: str
    range: str


class MeasureOut(MeasureIn):
    """
    Model of measure to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of measure returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
