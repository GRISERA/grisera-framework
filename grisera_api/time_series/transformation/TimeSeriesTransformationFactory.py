from time_series.transformation.TimeSeriesTransformationResample import TimeSeriesTransformationResample


class TimeSeriesTransformationFactory:
    """
    Factory to create time series transformation class

    """

    @staticmethod
    def get_transformation(transformation_name: str):
        """
        Transform time series data

        Args:
            transformation_name (str): Name of transformation

        Returns:
            New time series transformation class
        """
        if transformation_name == "resample":
            return TimeSeriesTransformationResample()
        else:
            raise Exception(f"transformation {transformation_name} is unknown")
