from typing import List
from pydantic import BaseModel
from typing import Optional, Any
from property.property_model import PropertyIn
from models.relation_information_model import RelationInformation


class ExperimentIn(BaseModel):
    """
    Model of experiment to acquire from client

    Attributes:
    experiment_name (str): Name of experiment
    additional_properties (Optional[List[PropertyIn]]): Additional properties for experiment
    """
    experiment_name: str
    additional_properties: Optional[List[PropertyIn]]


class BasicExperimentOut(ExperimentIn):
    """
    Basic model of experiment to send to client as a result of request

    Attributes:
    id (Optional[int]): Id of experiment returned from graph api
    """
    id: Optional[int]


class ExperimentOut(ExperimentIn):
    """
    Model of experiment with relationships to send to client as a result of request

    Attributes:
    relations (List[RelationInformation]): List of relations starting in experiment node
    reversed_relations (List[RelationInformation]): List of relations ending in experiment node
    errors (Optional[Any]): Optional errors appeared during query executions
    links (Optional[list]): List of links available from api
    """
    relations: List[RelationInformation] = []
    reversed_relations: List[RelationInformation] = []
    errors: Optional[Any] = None
    links: Optional[list] = None


class ExperimentsOut(BaseModel):
    """
    Model of experiments to send to client as a result of request

    Attributes:
    experiments (List[BasicExperimentOut]): Experiments from database
    errors (Optional[Any]): Optional errors appeared during query executions
    links (Optional[list]): List of links available from api
    """
    experiments: List[BasicExperimentOut] = []
    errors: Optional[Any] = None
    links: Optional[list] = None
