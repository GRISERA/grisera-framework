from pydantic import BaseModel
from typing import Optional, Any, List, Union
from enum import Enum
from models.relation_information_model import RelationInformation


class FacialHair(str, Enum):
    heavy = "Heavy"
    some = "Some"
    no = "No"


class AppearanceOcclusionIn(BaseModel):
    """
    Model of appearance occlusion to acquire from client

    Attributes:
        beard (FacialHair): Length of beard
        moustache (FacialHair): Length of moustache
    """
    beard: FacialHair
    moustache: FacialHair


class BasicAppearanceOcclusionOut(AppearanceOcclusionIn):
    """
    Basic model of appearance occlusion to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of appearance occlusion model returned from graph api
    """
    id: Optional[int]


class AppearanceOcclusionOut(BasicAppearanceOcclusionOut):
    """
    Model of appearance occlusion to send to client as a result of request

    Attributes:
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    errors: Optional[Any] = None
    links: Optional[list] = None


class AppearanceOcclusionRelationOut(BasicAppearanceOcclusionOut):
    """
    Model of appearance occlusion with relationships to send to client as a result of request

    Attributes:
        relations (List[RelationInformation]): List of relations starting in appearance node
        reversed_relations (List[RelationInformation]): List of relations ending in appearance node
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    relations: List[RelationInformation] = []
    reversed_relations: List[RelationInformation] = []
    errors: Optional[Any] = None
    links: Optional[list] = None


class AppearanceSomatotypeIn(BaseModel):
    """
    Model of appearance somatotype to acquire from client

    Attributes:
        glasses (bool): Does appearance contain glasses
        ectomorph (float): Range of ectomorph appearance measure
        endomorph (float): Range of endomorph appearance measure
        mesomorph (float): Range of mesomorph appearance measure

    """
    glasses: bool
    ectomorph: float
    endomorph: float
    mesomorph: float


class BasicAppearanceSomatotypeOut(AppearanceSomatotypeIn):
    """
    Basic model of appearance somatotype to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of appearance somatotype model returned from graph api

    """
    id: Optional[int]


class AppearanceSomatotypeOut(BasicAppearanceSomatotypeOut):
    """
    Model of appearance somatotype to send to client as a result of request

    Attributes:
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    errors: Optional[Any] = None
    links: Optional[list] = None


class AppearancesOut(BaseModel):
    """
    Model of appearances to send to client as a result of request

    Attributes:
        appearances (List[Union[BasicAppearanceSomatotypeOut, BasicAppearanceOcclusionOut]]): Appearances from database
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    appearances: List[Union[BasicAppearanceSomatotypeOut, BasicAppearanceOcclusionOut]] = []
    errors: Optional[Any] = None
    links: Optional[list] = None


class AppearanceSomatotypeRelationOut(BasicAppearanceSomatotypeOut):
    """
    Model of appearance somatotype with relationships to send to client as a result of request

    Attributes:
        relations (List[RelationInformation]): List of relations starting in appearance node
        reversed_relations (List[RelationInformation]): List of relations ending in appearance node
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    relations: List[RelationInformation] = []
    reversed_relations: List[RelationInformation] = []
    errors: Optional[Any] = None
    links: Optional[list] = None
