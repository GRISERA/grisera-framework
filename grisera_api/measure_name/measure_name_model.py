from pydantic import BaseModel
from typing import Optional, Any, List
from enum import Enum
from models.relation_information_model import RelationInformation


class MeasureName(tuple, Enum):
    """
    Names of measures with their types

    Attributes:
    familiarity (tuple): Familiarity
    liking (tuple): Liking
    anger (tuple): Anger
    disgust (tuple): Disgust
    fear (tuple): Fear
    happiness (tuple): Happiness
    sadness (tuple): Sadness
    surprise (tuple): Surprise
    neutral_state (tuple): Neutral state
    dominance (tuple): Dominance
    arousal (tuple): Arousal
    valence (tuple): Valence
    """
    familiarity = ("Familiarity", "Addional emotions measure")
    liking = ('Liking', "Ekman model measure")
    anger = ('Anger', "Ekman model measure")
    disgust = ('Disgust', "Ekman model measure")
    fear = ('Fear', "Ekman model measure")
    happiness = ('Happiness', "Ekman model measure")
    sadness = ('Sadness', "Ekman model measure")
    surprise = ('Surprise', "Ekman model measure")
    neutral_state = ('Neutral state', "Neutral state measure")
    dominance = ('Dominance', "PAD model measure")
    arousal = ('Arousal', "PAD model measure")
    valence = ('Valence', "PAD model measure")


class MeasureNameIn(BaseModel):
    """
    Model of measure name

    Attributes:
    name (str): Name of measure
    type (str): Type of the measure name
    """
    name: str
    type: str


class BasicMeasureNameOut(MeasureNameIn):
    """
    Model of measure name in database

    Attributes:
    id (Optional[int]): Id of measure name returned from graph api
    """
    id: Optional[int]


class MeasureNameOut(BasicMeasureNameOut):
    """
    Model of measure name to send to client as a result of request

    Attributes:
    relations (List[RelationInformation]): List of relations starting in registered data node
    reversed_relations (List[RelationInformation]): List of relations ending in registered data node
    errors (Optional[Any]): Optional errors appeared during query executions
    links (Optional[list]): List of links available from api
    """
    relations: List[RelationInformation] = []
    reversed_relations: List[RelationInformation] = []
    errors: Optional[Any] = None
    links: Optional[list] = None


class MeasureNamesOut(BaseModel):
    """
    Model of measure names to send to client as a result of request

    Attributes:
    measure_names (List[BasicMeasureNameOut]): Measure names from database
    errors (Optional[Any]): Optional errors appeared during query executions
    links (Optional[list]): List of links available from api
    """
    measure_names: List[BasicMeasureNameOut] = []
    errors: Optional[Any] = None
    links: Optional[list] = None
