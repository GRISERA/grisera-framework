from typing import List
from pydantic import BaseModel
from typing import Optional, Any
from property.property_model import PropertyIn
from author.author_model import AuthorIn, AuthorOut
from publication.publication_model import PublicationIn, PublicationOut


class ExperimentIn(BaseModel):
    """
    Model of experiment to acquire from client

    Attributes:
        experiment_name (str): Name of experiment
        authors (Optional[Set[AuthorIn]]): Authors of the experiment
        publication(Optional[PublicationIn]): Publication, in which the experiment is described
        abstract (Optional[str]): Summary of the experiment
        additional_properties (Optional[List[PropertyIn]]): Additional properties for experiment
    """
    experiment_name: str
    authors: Optional[List[AuthorIn]]
    publication: Optional[PublicationIn]
    abstract: Optional[str]
    additional_properties: Optional[List[PropertyIn]]


class ExperimentOut(ExperimentIn):
    """
    Model of experiment to send to client as a result of request

    Attributes:
        authors (Optional[Set[AuthorOut]]): Authors of the experiment
        publication(Optional[Publicationout]): Publication, in which the experiment is described
        id (Optional[int]): Id of experiment returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    authors: Optional[List[AuthorOut]]
    publication: Optional[PublicationOut]
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
