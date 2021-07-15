from pydantic import BaseModel
from typing import Optional, Any
from modality.modality_model import Modality
from live_activity.live_activity_model import LiveActivity


class ObservableInformationIn(BaseModel):
    """
    Model of information observed during experiment

    Attributes:
        modality (Modality): Type of observable information
        live_activity (LiveActivity): Actions of a human body
    """
    modality: Modality
    live_activity: LiveActivity


class ObservableInformationOut(ObservableInformationIn):
    """
    Model of information observed during experiment to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of node returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
