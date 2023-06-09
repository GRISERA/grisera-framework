from typing import Optional, Union, List

from pydantic import BaseModel

from models.base_model_out import BaseModelOut


class MeasurePropertyIn(BaseModel):
    """
    Model of measure to acquire from client

    Attributes:
    datatype (str): Type of data
    range (str): Range of measure
    unit (str): Datatype property which allows for defining unit of measure
    """

    datatype: str
    range: str
    unit: str


class MeasureRelationIn(BaseModel):
    """
    Model of measure relations to acquire from client

    Attributes:
    measure_name_id (int | str): identity of the measure name
    """

    measure_name_id: Optional[Union[int, str]]


class MeasureIn(MeasurePropertyIn, MeasureRelationIn):
    """
    Full model of measure to acquire from client
    """


class BasicMeasureOut(MeasurePropertyIn):
    """
    Basic model of measure

    Attributes:
    id (Optional[Union[int, str]]): Id of measure returned from api
    """

    id: Optional[Union[int, str]]


class MeasureOut(BasicMeasureOut, BaseModelOut):
    """
    Model of measure with relations to send to client as a result of request

    Attributes:
    time_series (Optional[List[SignalSeriesOut]]): list of time series related to this measure
    measure_name (Optional[MeasureNameOut]): measure name related to this measure
    """

    time_series: "Optional[List[SignalSeriesOut]]"
    measure_name: "Optional[MeasureNameOut]"


class MeasuresOut(BaseModelOut):
    """
    Model of measures to send to client as a result of request

    Attributes:
    measures (List[BasicMeasureOut]): measures from database
    """

    measures: List[BasicMeasureOut] = []


# Circular import exception prevention
from measure_name.measure_name_model import MeasureNameOut
from signal_series.signal_series_model import SignalSeriesOut

MeasureOut.update_forward_refs()
