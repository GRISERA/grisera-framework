from enum import Enum
from typing import List, Optional

from property.property_model import PropertyIn
from time_series.time_series_model import TimeSeriesOut


class TransformationType(str, Enum):
    """
    The type of transformation
    """
    RESAMPLE_NEAREST = "resample_nearest"
    QUADRANTS = "quadrants"


class TimeSeriesTransformation:
    """
    Abstract class to handle logic of time series transformation

    """

    def transform(self, time_series: List[TimeSeriesOut], additional_properties: Optional[List[PropertyIn]]):
        """
        Transform time series data

        Args:
            time_series (List[TimeSeriesOut]): Time series to be transformed
            additional_properties (Optional[List[PropertyIn]]): Transformation parameters

        Returns:
            New time series object
        """
        raise Exception("transform not implemented yet")
