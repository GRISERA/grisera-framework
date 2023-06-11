from enum import Enum
from typing import Optional, List, Union

from pydantic import BaseModel

from models.base_model_out import BaseModelOut
from property.property_model import PropertyIn


class TransformationType(str, Enum):
    """
    The type of transformation
    """
    RESAMPLE_NEAREST = "resample_nearest"
    QUADRANTS = "quadrants"
    FOURIER = "fourier"


class StampNodesIn(BaseModel):
    """
    Model of timestamp node
    Attributes:
        timestamp (int): Timestamp of signal measure in milliseconds
    """
    timestamp: Optional[int]
    frequencystamp: Optional[int]


class SignalValueNodesIn(BaseModel):
    """
    Model of signal value node
    Attributes:
        value (Union[str, float]): Value of signal
        additional_properties (Optional[List[PropertyIn]]): Additional properties for signal value
    """
    value: Union[str, float]
    additional_properties: Optional[List[PropertyIn]]


class SignalIn(BaseModel):
    """
    Model of signal to acquire from client
    Attributes:
        timestamp (Optional[int]): Timestamp of signal measure of type Timestamp in milliseconds
        start_timestamp (Optional[int]): Timestamp of begin signal measure of type Epoch in milliseconds
        end_timestamp (Optional[int]): Timestamp of end signal measure of type Epoch in milliseconds
        signal_value (SignalValueNodesIn): Value of signal
    """
    timestamp: Optional[int]
    start_timestamp: Optional[int]
    end_timestamp: Optional[int]
    frequencystamp: Optional[int]
    signal_value: SignalValueNodesIn


class Type(str, Enum):
    """
    Types of time series

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
    frequencystamp = "Frequencystamp"


class SignalSeriesPropertyIn(BaseModel):
    """
    Model of time series to acquire from client

    Attributes:
        type (Type): Type of the signal
        source (str): TimeSeries source
        signal_values (List[SignalIn]): list of signals
        additional_properties (Optional[List[PropertyIn]]): Additional properties for signal
    """
    type: Type
    source: Optional[str]
    signal_values: List[SignalIn] = []
    additional_properties: Optional[List[PropertyIn]]


class SignalSeriesTransformationIn(BaseModel):
    """
    Model of time series transformation to acquire from client

    Attributes:
        name (TransformationType): Name of the transformation
        source_time_series_ids (List[int]): Ids of source time series
        destination_observable_information_id (Optional[int]): Id of destination observable information
        destination_measure_id (Optional[int]): Id of destination measure
        additional_properties (Optional[List[PropertyIn]]): Additional properties for transformation
    """
    name: TransformationType
    source_time_series_ids: List[int]
    destination_observable_information_id: Optional[int]
    destination_measure_id: Optional[int]
    additional_properties: Optional[List[PropertyIn]]


class SignalSeriesTransformationRelationshipIn(BaseModel):
    """
    Model of time series transformation relationship

    Attributes:
        additional_properties (Optional[List[PropertyIn]]): Additional properties for transformation
    """
    additional_properties: Optional[List[PropertyIn]]


class SignalSeriesRelationIn(BaseModel):
    """
    Model of time series relations to acquire from client

    Attributes:
        observable_information_id (Optional[Union[int, str]]): Id of observable information
        measure_id (Optional[Union[int, str]]): Id of measure
    """
    observable_information_id: Optional[Union[int, str]]
    measure_id: Optional[Union[int, str]]


class SignalSeriesIn(SignalSeriesPropertyIn, SignalSeriesRelationIn):
    """
    Full model of time series to acquire from client
    """


class BasicSignalSeriesOut(SignalSeriesPropertyIn, BaseModelOut):
    """
    Basic model of time series

    Attributes:
    id (Optional[Union[int, str]]): Id of time series returned from api
    signal_values (list): list of signals
    """

    id: Optional[Union[int, str]]
    signal_values: list = []


class SignalSeriesOut(BasicSignalSeriesOut, BaseModelOut):
    """
    Model of time series with relations to send to client as a result of request

    Attributes:
        observable_informations (Optional[List[ObservableInformationOut]]): List of observable informations related to
            this time series
        measure (Optional[MeasureOut]): measure related to this time series
    """

    observable_informations: "Optional[List[ObservableInformationOut]]"
    measure: "Optional[MeasureOut]"


class SignalSeriesMultidimensionalOut(BaseModelOut):
    """
    Model of time multidimensional series to send to client as a result of request

    Attributes:
        signal_values (list): List of signal values
        time_series (List[SignalSeriesOut]): Time series nodes from database
    """
    signal_values: list = []
    time_series: List[SignalSeriesOut] = []


class SignalSeriesNodesOut(BaseModelOut):
    """
    Model of time series nodes to send to client as a result of request

    Attributes:
        time_series_nodes (List[BasicSignalSeriesOut]): Time series nodes from database
    """
    time_series_nodes: List[BasicSignalSeriesOut] = []


# Circular import exception prevention
from measure.measure_model import MeasureOut
from observable_information.observable_information_model import ObservableInformationOut

SignalSeriesOut.update_forward_refs()