from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum


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


class AppearanceOcclusionOut(AppearanceOcclusionIn):
    """
    Model of appearance occlusion to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of appearance occlusion model returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
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


class AppearanceSomatotypeOut(AppearanceSomatotypeIn):
    """
    Model of appearance somatotype to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of appearance somatotype model returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
