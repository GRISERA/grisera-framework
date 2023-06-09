from typing import List, Optional

from property.property_model import PropertyIn
from signal_series.signal_series_model import SignalSeriesOut


class TimeSeriesTransformation:
    """
    Abstract class to handle logic of time series transformation

    """

    def transform(self, time_series: List[SignalSeriesOut], additional_properties: Optional[List[PropertyIn]]):
        """
        Transform time series data

        Args:
            time_series (List[SignalSeriesOut]): Time series to be transformed
            additional_properties (Optional[List[PropertyIn]]): Transformation parameters

        Returns:
            New time series object
        """
        raise Exception("transform not implemented yet")
