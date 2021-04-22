from typing import List
from pydantic import BaseModel
from typing import Optional, Any
from author.author_model import AuthorIn


class PublicationIn(BaseModel):
    """
    Model of publication to acquire from client

    Attributes:
        title (str): Title of the publication
        authors (List[AuthorIn]): Authors of the publication
    """
    title: str
    authors: List[AuthorIn]


class PublicationOut(PublicationIn):
    """
    Model of publication to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of publication returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
