from pydantic import BaseModel
from typing import Optional, Any, List
from enum import Enum
from property.property_model import PropertyIn


class Type(str, Enum):
    """
    Types of signal

    Attributes:
        epoch (str): Epoch signal
        irregularly_spaced (str): Irregularly spaced signal
        regularly_spaced (str): Regularly spaced signal
        timestamp (str): Timestamp signal
    """
    epoch = "Epoch"
    irregularly_spaced = "Irregularly spaced"
    regularly_spaced = "Regularly spaced"
    timestamp = "Timestamp"


class TimeSeriesIn(BaseModel):
    """
    Model of signal

    Attributes:
        type (Type): Type of the signal
        source(str): TimeSeries source
        observable_information_id (Optional[int]): Id of observable information
        measure_id (Optional[int]): Id of measure
        additional_properties (Optional[List[PropertyIn]]): Additional properties for signal
    """
    type: Type
    source: str
    observable_information_id: Optional[int]
    measure_id: Optional[int]
    additional_properties: Optional[List[PropertyIn]]


class TimeSeriesOut(TimeSeriesIn):
    """
    Model of signal to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of signal returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
