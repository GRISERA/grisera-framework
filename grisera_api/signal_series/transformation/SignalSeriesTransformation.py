from typing import List, Optional

from property.property_model import PropertyIn
from signal_series.signal_series_model import SignalSeriesOut


class SignalSeriesTransformation:
    """
    Abstract class to handle logic of signal series transformation

    """

    def transform(self, signal_series: List[SignalSeriesOut], additional_properties: Optional[List[PropertyIn]]):
        """
        Transform signal series data

        Args:
            signal_series (List[SignalSeriesOut]): Time series to be transformed
            additional_properties (Optional[List[PropertyIn]]): Transformation parameters

        Returns:
            New signal series object
        """
        raise Exception("transform not implemented yet")
