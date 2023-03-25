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
from participation.participation_model import ParticipationIn
from personality.personality_model import (
    PersonalityBigFiveIn,
    PersonalityPanasIn,
)
from recording.recording_model import (
    RecordingPropertyIn,
    RecordingRelationIn,
)
from registered_channel.registered_channel_model import RegisteredChannelIn
from registered_data.registered_data_model import RegisteredDataIn
from scenario.scenario_model import ScenarioIn
from time_series.time_series_model import (
    TimeSeriesPropertyIn,
    TimeSeriesRelationIn,
)


SUPERCLASSES_TO_COLLECTION_NAMES = {
    ActivityIn: "activities",
    ActivityExecutionPropertyIn: "activity_executions",
    ActivityExecutionRelationIn: "activity_executions",
    AppearanceOcclusionIn: "appearances",
    AppearanceSomatotypeOut: "appearances",
    ArrangementIn: "arrangements",
    ChannelIn: "channels",
    ExperimentIn: "experiments",
    LifeActivityIn: "life_activities",
    MeasurePropertyIn: "measures",
    MeasureRelationIn: "measures",
    MeasureNameIn: "measure_names",
    ModalityIn: "modalities",
    ObservableInformationIn: "observable_informations",
    ParticipantIn: "participants",
    ParticipantStatePropertyIn: "participant_states",
    ParticipantStateRelationIn: "participant_states",
    ParticipationIn: "participations",
    PersonalityBigFiveIn: "personalities",
    PersonalityPanasIn: "personalities",
    RecordingPropertyIn: "recordings",
    RecordingRelationIn: "recordings",
    RegisteredChannelIn: "registered_channels",
    RegisteredDataIn: "registered_data",
    ScenarioIn: "scenarios",
    TimeSeriesPropertyIn: "time_series",
    TimeSeriesRelationIn: "time_series",
}


def get_collection_name(model_class):
    """
    Get mongo collection name, based on the class of model object
    """
    for superclass, collection_name in SUPERCLASSES_TO_COLLECTION_NAMES.items():
        if issubclass(model_class, superclass):
            return collection_name
    raise ValueError("Given class is not subclass of any model")
