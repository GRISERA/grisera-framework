from signal_series.signal_series_model import TransformationType
from signal_series.transformation.SignalSeriesTransformationQuadrants import SignalSeriesTransformationQuadrants
from signal_series.transformation.SignalSeriesTransformationResample import SignalSeriesTransformationResample
from signal_series.transformation.SignalSeriesTransformationFourier import SignalSeriesTransformationFourier


class SignalSeriesTransformationFactory:
    """
    Factory to create signal series transformation class

    """

    @staticmethod
    def get_transformation(transformation_name: str):
        """
        Transform signal series data

        Args:
            transformation_name (str): Name of transformation

        Returns:
            New signal series transformation class
        """
        if transformation_name == TransformationType.RESAMPLE_NEAREST:
            return SignalSeriesTransformationResample()
        elif transformation_name == TransformationType.QUADRANTS:
            return SignalSeriesTransformationQuadrants()
        elif transformation_name == TransformationType.FOURIER:
            return SignalSeriesTransformationFourier()
        else:
            raise Exception(f"transformation {transformation_name} is unknown")
