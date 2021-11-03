from pydantic import BaseModel
from typing import Optional, Any, List
from enum import Enum


class Arrangement(tuple, Enum):
    """
    The type of arrangement

    Attributes:
        casual_personal_zone (tuple): Personal two persons arrangement - casual personal zone
        intimate_zone (tuple): Personal two persons arrangement - intimate zone
        public_zone (tuple): Personal two persons arrangement - public zone
        socio_consultive_zone (tuple): Personal two persons arrangement - socio consultive zone
        personal_group (tuple): Personal group arrangement
    """
    casual_personal_zone = ("personal two persons", "casual personal zone")
    intimate_zone = ("personal two persons", "intimate zone")
    public_zone = ("personal two persons", "public zone")
    socio_consultive_zone = ("personal two persons", "socio consultive zone")
    personal_group = ("personal group", None)


class ArrangementIn(BaseModel):
    """
    Model of arrangement

    Attributes:
        arrangement (str): Type of arrangement
    """
    arrangement_type: str
    arrangement_distance: Optional[str]


class BasicArrangementOut(ArrangementIn):
    """
    Model of arrangement in database

    Attributes:
        id (Optional[int]): Id of arrangement returned from graph api
    """
    id: Optional[int]


class ArrangementOut(BasicArrangementOut):
    """
    Model of arrangement to send to client as a result of request

    Attributes:
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    errors: Optional[Any] = None
    links: Optional[list] = None


class ArrangementsOut(BaseModel):
    """
    Model of activities to send to client as a result of request

    Attributes:
        arrangement_types (List[BasicArrangementOut]): Arrangement types from database
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    arrangements: List[BasicArrangementOut] = []
    errors: Optional[Any] = None
    links: Optional[list] = None
