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
    Model of stamp node
    Attributes:
        timestamp (int): Timestamp of signal measure in milliseconds
        frequencystamp (int): Frequency of signal measure in Hz
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
    Types of signal series

    Attributes:
        epoch (str): Epoch signal
        irregularly_spaced (str): Irregularly spaced signal
        regularly_spaced (str): Regularly spaced signal
        timestamp (str): Timestamp signal
        frequencystamp (str): Frequencystamp signal
    """
    epoch = "Epoch"
    irregularly_spaced = "Irregularly spaced"
    regularly_spaced = "Regularly spaced"
    timestamp = "Timestamp"
    frequencystamp = "Frequencystamp"


class SignalSeriesPropertyIn(BaseModel):
    """
    Model of signal series to acquire from client

    Attributes:
        type (Type): Type of the signal
        source (str): SignalSeries source
        signal_values (List[SignalIn]): list of signals
        additional_properties (Optional[List[PropertyIn]]): Additional properties for signal
    """
    type: Type
    source: Optional[str]
    signal_values: List[SignalIn] = []
    additional_properties: Optional[List[PropertyIn]]


class SignalSeriesTransformationIn(BaseModel):
    """
    Model of signal series transformation to acquire from client

    Attributes:
        name (TransformationType): Name of the transformation
        source_signal_series_ids (List[int]): Ids of source signal series
        destination_observable_information_id (Optional[int]): Id of destination observable information
        destination_measure_id (Optional[int]): Id of destination measure
        additional_properties (Optional[List[PropertyIn]]): Additional properties for transformation
    """
    name: TransformationType
    source_signal_series_ids: List[int]
    destination_observable_information_id: Optional[int]
    destination_measure_id: Optional[int]
    additional_properties: Optional[List[PropertyIn]]


class SignalSeriesTransformationRelationshipIn(BaseModel):
    """
    Model of signal series transformation relationship

    Attributes:
        additional_properties (Optional[List[PropertyIn]]): Additional properties for transformation
    """
    additional_properties: Optional[List[PropertyIn]]


class SignalSeriesRelationIn(BaseModel):
    """
    Model of signal series relations to acquire from client

    Attributes:
        observable_information_id (Optional[Union[int, str]]): Id of observable information
        measure_id (Optional[Union[int, str]]): Id of measure
    """
    observable_information_id: Optional[Union[int, str]]
    measure_id: Optional[Union[int, str]]


class SignalSeriesIn(SignalSeriesPropertyIn, SignalSeriesRelationIn):
    """
    Full model of signal series to acquire from client
    """


class BasicSignalSeriesOut(SignalSeriesPropertyIn, BaseModelOut):
    """
    Basic model of signal series

    Attributes:
    id (Optional[Union[int, str]]): Id of signal series returned from api
    signal_values (list): list of signals
    """

    id: Optional[Union[int, str]]
    signal_values: list = []


class SignalSeriesOut(BasicSignalSeriesOut, BaseModelOut):
    """
    Model of signal series with relations to send to client as a result of request

    Attributes:
        observable_informations (Optional[List[ObservableInformationOut]]): List of observable informations related to
            this signal series
        measure (Optional[MeasureOut]): measure related to this signal series
    """

    observable_informations: "Optional[List[ObservableInformationOut]]"
    measure: "Optional[MeasureOut]"


class SignalSeriesMultidimensionalOut(BaseModelOut):
    """
    Model of signal multidimensional series to send to client as a result of request

    Attributes:
        signal_values (list): List of signal values
        signal_series (List[SignalSeriesOut]): signal series nodes from database
    """
    signal_values: list = []
    signal_series: List[SignalSeriesOut] = []


class SignalSeriesNodesOut(BaseModelOut):
    """
    Model of signal series nodes to send to client as a result of request

    Attributes:
        signal_series_nodes (List[BasicSignalSeriesOut]): signal series nodes from database
    """
    signal_series_nodes: List[BasicSignalSeriesOut] = []


# Circular import exception prevention
from measure.measure_model import MeasureOut
from observable_information.observable_information_model import ObservableInformationOut

SignalSeriesOut.update_forward_refs()