from typing import Optional, Any, List

from pydantic import BaseModel

from models.relation_information_model import RelationInformation


class MeasurePropertyIn(BaseModel):
    """
    Model of measure to acquire from client

    Attributes:
    datatype (str): Type of data
    range (str): Range of measure
    unit (Optional[str]): Datatype property which allows for defining unit of measure
    """
    datatype: str
    range: str
    unit: Optional[str]


class MeasureRelationIn(BaseModel):
    """
    Model of measure relations to acquire from client

    Attributes:
    measure_name_id (int): Id of the measure name
    """
    measure_name_id: Optional[int]


class MeasureIn(MeasurePropertyIn, MeasureRelationIn):
    """
    Full model of measure to acquire from client
    """


class BasicMeasureOut(MeasurePropertyIn):
    """
    Basic model of measure

    Attributes:
        id (Optional[int]): Id of measure returned from graph api
    """
    id: Optional[int]


class MeasureOut(BasicMeasureOut):
    """
    Model of measure with relations to send to client as a result of request

    Attributes:
        relations (List[RelationInformation]): List of relations starting in measure node
        reversed_relations (List[RelationInformation]): List of relations ending in measure node
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    relations: List[RelationInformation] = []
    reversed_relations: List[RelationInformation] = []
    errors: Optional[Any] = None
    links: Optional[list] = None


class MeasuresOut(BaseModel):
    """
    Model of measures to send to client as a result of request

    Attributes:
        measures (List[BasicMeasureOut]): measures from database
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    measures: List[BasicMeasureOut] = []
    errors: Optional[Any] = None
    links: Optional[list] = None
