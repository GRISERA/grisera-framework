from pydantic import BaseModel
from typing import Optional, Any, List
from enum import Enum
from property.property_model import PropertyIn
from models.relation_information_model import RelationInformation


class Modality(str, Enum):
    """
    Type of observable information

    Attributes:
        facial_expressions (str): Facial expressions
        body_posture (str): Body posture
        eye_gaze (str): Eye gaze
        head_movement (str): Head movement
        gestures (str): Gestures
        motion (str): Motion
        prosody_of_speech (str): Prosody of speech
        vocalization (str): Vocalization
        heart_rate (str): Heart rate
        hrv (str): HRV
        muscle_tension (str): Muscle tension
        skin_conductance (str): Skin conductance
        resp_intensity_and_period (str): RESP intensity and period
        peripheral_temperature (str): Peripheral temperature
        neural_activity (str): Neural activity
    """
    facial_expressions = "facial expressions"
    body_posture = "body posture"
    eye_gaze = "eye gaze"
    head_movement = "head movement"
    gestures = "gestures"
    motion = "motion"
    prosody_of_speech = "prosody of speech"
    vocalization = "vocalization"
    heart_rate = "heart rate"
    hrv = "HRV"
    muscle_tension = "muscle tension"
    skin_conductance = "skin conductance"
    resp_intensity_and_period = "RESP intensity and period"
    peripheral_temperature = "peripheral temperature"
    neural_activity = "neural activity"


class ModalityIn(BaseModel):
    """
    Model of modality observed during experiment

    Attributes:
    modality (str): Type of observable information
    """
    modality: str


class BasicModalityOut(ModalityIn):
    """
    Model of modality in database

    Attributes:
    id (Optional[int]): Id of modality returned from graph api
    """
    id: Optional[int]


class ModalityOut(BasicModalityOut):
    """
    Model of information observed during experiment to send to client as a result of request

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


class ModalitiesOut(BaseModel):
    """
    Model of information observed during experiment to send to client as a result of request

    Attributes:
        modalities (List[BasicModalityOut]): Modalities from database
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    modalities: List[BasicModalityOut] = []
    errors: Optional[Any] = None
    links: Optional[list] = None
