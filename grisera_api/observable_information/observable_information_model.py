from pydantic import BaseModel
from typing import Optional, Any
from enum import Enum


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


class LiveActivity(str, Enum):
    """
    Actions of a human body

    Attributes:
        movement (str): Movement
        sound (str): Sound
        heart_activity (str): Heart activity
        muscles_activity (str): Muscles activity
        perspiration (str): Perspiration
        respiration (str): Respiration
        thermal_regulation (str): Thermal regulation
        brain_activity (str): Brain activity
    """
    movement = "movement"
    sound = "sound"
    heart_activity = "heart activity"
    muscles_activity = "muscles activity"
    perspiration = "perspiration"
    respiration = "respiration"
    thermal_regulation = "thermal regulation"
    brain_activity = "brain activity"


class ObservableInformationIn(BaseModel):
    """
    Model of information observed during experiment

    Attributes:
        modality (Modality): Type of observable information
        live_activity (LiveActivity): Actions of a human body
    """
    modality: Modality
    live_activity: LiveActivity


class ObservableInformationOut(ObservableInformationIn):
    """
    Model of information observed during experiment to send to client as a result of request

    Attributes:
        id (Optional[int]): Id of node returned from graph api
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list]): List of links available from api
    """
    id: Optional[int]
    errors: Optional[Any] = None
    links: Optional[list] = None
