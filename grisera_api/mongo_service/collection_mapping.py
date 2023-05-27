from activity.activity_model import ActivityIn
from activity_execution.activity_execution_model import (
    ActivityExecutionPropertyIn,
    ActivityExecutionRelationIn,
)
from appearance.appearance_model import (
    AppearanceOcclusionIn,
    AppearanceSomatotypeOut,
)
from arrangement.arrangement_model import ArrangementIn
from channel.channel_model import ChannelIn
from experiment.experiment_model import ExperimentIn
from life_activity.life_activity_model import LifeActivityIn
from measure.measure_model import MeasurePropertyIn, MeasureRelationIn
from measure_name.measure_name_model import MeasureNameIn
from modality.modality_model import ModalityIn
from observable_information.observable_information_model import (
    ObservableInformationIn,
)
from participant.participant_model import ParticipantIn
from participant_state.participant_state_model import (
    ParticipantStatePropertyIn,
    ParticipantStateRelationIn,
)
from participation.participation_model import ParticipationIn, BasicParticipationOut
from personality.personality_model import (
    PersonalityBigFiveIn,
    PersonalityPanasIn,
)
from recording.recording_model import (
    RecordingPropertyIn,
    RecordingRelationIn,
)
from registered_channel.registered_channel_model import (
    RegisteredChannelIn,
    BasicRegisteredChannelOut,
)
from registered_data.registered_data_model import RegisteredDataIn
from scenario.scenario_model import ScenarioIn
from time_series.time_series_model import (
    TimeSeriesPropertyIn,
    TimeSeriesRelationIn,
)
from enum import Enum

"""
This module provides enum with collection names in mongodb to help avoiding 
possible errors with typos in collection names strings.

It also provides mapping of model classes to collection names. It is useful 
as it allows to dynamically determine collection name based on model objets 
class.
"""


class Collections(str, Enum):
    ACTIVITY = "activities"
    ACTIVITY_EXECUTION = "activity_executions"
    APPEARANCE = "appearances"
    ARRANGEMENT = "arrangements"
    CHANNEL = "channels"
    EXPERIMENT = "experiments"
    LIFE_ACTIVITY = "life_activities"
    MEASURE = "measures"
    MEASURE_NAME = "measure_names"
    MODALITY = "modalities"
    OBSERVABLE_INFORMATION = "observable_informations"
    PARTICIPANT = "participants"
    PARTICIPANT_STATE = "participant_states"
    PARTICIPATION = "participations"
    PERSONALITY = "personalities"
    RECORDING = "recordings"
    REGISTERED_CHANNEL = "registered_channels"
    REGISTERED_DATA = "registered_data"
    SCENARIO = "scenarios"
    TIME_SERIES = "TimeSeries"


SUPERCLASSES_TO_COLLECTION_NAMES = {
    ActivityIn: Collections.ACTIVITY,
    ActivityExecutionPropertyIn: Collections.ACTIVITY_EXECUTION,
    ActivityExecutionRelationIn: Collections.ACTIVITY_EXECUTION,
    AppearanceOcclusionIn: Collections.APPEARANCE,
    AppearanceSomatotypeOut: Collections.APPEARANCE,
    ArrangementIn: Collections.ARRANGEMENT,
    ChannelIn: Collections.CHANNEL,
    ExperimentIn: Collections.EXPERIMENT,
    LifeActivityIn: Collections.LIFE_ACTIVITY,
    MeasurePropertyIn: Collections.MEASURE,
    MeasureRelationIn: Collections.MEASURE,
    MeasureNameIn: Collections.MEASURE_NAME,
    ModalityIn: Collections.MODALITY,
    ObservableInformationIn: Collections.OBSERVABLE_INFORMATION,
    ParticipantIn: Collections.PARTICIPANT,
    ParticipantStatePropertyIn: Collections.PARTICIPANT_STATE,
    ParticipantStateRelationIn: Collections.PARTICIPANT_STATE,
    BasicParticipationOut: Collections.PARTICIPATION,
    ParticipationIn: Collections.PARTICIPATION,
    PersonalityBigFiveIn: Collections.PERSONALITY,
    PersonalityPanasIn: Collections.PERSONALITY,
    RecordingPropertyIn: Collections.RECORDING,
    RecordingRelationIn: Collections.RECORDING,
    BasicRegisteredChannelOut: Collections.REGISTERED_CHANNEL,
    RegisteredChannelIn: Collections.REGISTERED_CHANNEL,
    RegisteredDataIn: Collections.REGISTERED_DATA,
    ScenarioIn: Collections.SCENARIO,
    TimeSeriesPropertyIn: Collections.TIME_SERIES,
    TimeSeriesRelationIn: Collections.TIME_SERIES,
}


def get_collection_name(model_class):
    """
    Get mongo collection name, based on the class of model object
    """
    for superclass, collection_name in SUPERCLASSES_TO_COLLECTION_NAMES.items():
        if issubclass(model_class, superclass):
            return collection_name
    raise ValueError(f"{model_class} class is not subclass of any model")
