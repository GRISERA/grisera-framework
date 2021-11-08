from pydantic import BaseModel
from typing import Optional, Any, List
from models.relation_information_model import RelationInformation


class ObservableInformationIn(BaseModel):
    """
    Model of information observed during experiment

    Attributes:
        modality (Modality): Type of observable information
        live_activity (LiveActivity): Actions of a human body
        recording_id (Optional[int]): Id of recording
    """
    modality: str
    live_activity: str
    recording_id: Optional[int]


class BasicObservableInformationOut(ObservableInformationIn):
    """
    Model of information observed during experiment in database

    Attributes:
    id (Optional[int]): Id of node returned from graph api
    """
    id: Optional[int]


class ObservableInformationOut(BasicObservableInformationOut):
    """
    Model of information observed during experiment to send to client as a result of request

    Attributes:

    relations (List[RelationInformation]): List of relations starting in observable information node
    reversed_relations (List[RelationInformation]): List of relations ending in observable information node
    errors (Optional[Any]): Optional errors appeared during query executions
    links (Optional[list]): List of links available from api
    """
    relations: List[RelationInformation] = []
    reversed_relations: List[RelationInformation] = []
    errors: Optional[Any] = None
    links: Optional[list] = None


class ObservableInformationsOut(BaseModel):
    """
    Model of information observed during experiment to send to client as a result of request
    Attributes:
    live_activities (List[BasicLiveActivityOut]): Live activities from database
    errors (Optional[Any]): Optional errors appeared during query executions
    links (Optional[list]): List of links available from api
    """
    observable_informations: List[BasicObservableInformationOut] = []
    errors: Optional[Any] = None
    links: Optional[list] = None
