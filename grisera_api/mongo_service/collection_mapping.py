from grisera_api.activity.activity_model import ActivityIn
from grisera_api.activity_execution.activity_execution_model import (
    ActivityExecutionPropertyIn,
    ActivityExecutionRelationIn,
)
from grisera_api.appearance.appearance_model import (
    AppearanceOcclusionIn,
    AppearanceSomatotypeOut,
)
from grisera_api.arrangement.arrangement_model import ArrangementIn
from grisera_api.channel.channel_model import ChannelIn
from grisera_api.experiment.experiment_model import ExperimentIn
from grisera_api.life_activity.life_activity_model import LifeActivityIn
from grisera_api.measure.measure_model import MeasurePropertyIn, MeasureRelationIn
from grisera_api.measure_name.measure_name_model import MeasureNameIn
from grisera_api.modality.modality_model import ModalityIn
from grisera_api.observable_information.observable_information_model import (
    ObservableInformationIn,
)
from grisera_api.participant.participant_model import ParticipantIn
from grisera_api.participant_state.participant_state_model import (
    ParticipantStatePropertyIn,
    ParticipantStateRelationIn,
)
from grisera_api.participation.participation_model import ParticipationIn
from grisera_api.personality.personality_model import (
    PersonalityBigFiveIn,
    PersonalityPanasIn,
)
from grisera_api.recording.recording_model import (
    RecordingPropertyIn,
    RecordingRelationIn,
)
from grisera_api.registered_channel.registered_channel_model import RegisteredChannelIn
from grisera_api.registered_data.registered_data_model import RegisteredDataIn
from grisera_api.scenario.scenario_model import ScenarioIn
from grisera_api.time_series.time_series_model import (
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
