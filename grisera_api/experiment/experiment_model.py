from typing import List
from pydantic import BaseModel
from typing import Optional, Any
from property.property_model import PropertyIn
from author.author_model import AuthorIn
from publication.publication_model import PublicationIn



class ExperimentIn(BaseModel):
    """
    Model of experiment to acquire from client

    Attributes:
        name (str): Name of experiment
        authors (Optional[Set[AuthorIn]]): Authors of the experiment
        publication(Optional[PublicationIn]): Publication, in which the experiment is described
        abstract (Optional[str]): Summary of the experiment
        additional_properties (Optional[List[PropertyIn]]): Additional properties for experiment
    """
    name: str
    authors: Optional[List[AuthorIn]]
    publication: Optional[PublicationIn]
    abstract: Optional[str]
    additional_properties: Optional[List[PropertyIn]]


class ExperimentOut(ExperimentIn):
    """
    Model of experiment to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of experiment returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
