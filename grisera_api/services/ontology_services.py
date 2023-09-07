from services.service_factory import ServiceFactory
from activity.activity_service import ActivityService
from activity.activity_service_ontology import ActivityServiceOntology
from activity_execution.activity_execution_service import ActivityExecutionService
from activity_execution.activity_execution_service_ontology import (
    ActivityExecutionServiceOntology,
)
from appearance.appearance_service import AppearanceService
from appearance.appearance_service_ontology import AppearanceServiceOntology
from arrangement.arrangement_service import ArrangementService
from arrangement.arrangement_service_ontology import ArrangementServiceOntology
from channel.channel_service import ChannelService
from channel.channel_service_ontology import ChannelServiceOntology
from dataset.dataset_service import DatasetService
from dataset.dataset_service_ontology import DatasetServiceOntology
from experiment.experiment_service import ExperimentService
from experiment.experiment_service_ontology import ExperimentServiceOntology
from life_activity.life_activity_service import LifeActivityService
from life_activity.life_activity_service_ontology import LifeActivityServiceOntology
from measure.measure_service import MeasureService
from measure.measure_service_ontology import MeasureServiceOntology
from measure_name.measure_name_service import MeasureNameService
from measure_name.measure_name_service_ontology import MeasureNameServiceOntology
from modality.modality_service import ModalityService
from modality.modality_service_ontology import ModalityServiceOntology
from observable_information.observable_information_service import (
    ObservableInformationService,
)
from observable_information.observable_information_service_ontology import (
    ObservableInformationServiceOntology,
)
from participant.participant_service import ParticipantService
from participant.participant_service_ontology import ParticipantServiceOntology
from participant_state.participant_state_service import ParticipantStateService
from participant_state.participant_state_service_ontology import (
    ParticipantStateServiceOntology,
)
from participation.participation_service import ParticipationService
from participation.participation_service_ontology import ParticipationServiceOntology
from personality.personality_service import PersonalityService
from personality.personality_service_ontology import PersonalityServiceOntology
from recording.recording_service import RecordingService
from recording.recording_service_ontology import RecordingServiceOntology
from registered_channel.registered_channel_service import RegisteredChannelService
from registered_channel.registered_channel_service_ontology import (
    RegisteredChannelServiceOntology,
)
from registered_data.registered_data_service import RegisteredDataService
from registered_data.registered_data_service_ontology import (
    RegisteredDataServiceOntology,
)
from scenario.scenario_service import ScenarioService
from scenario.scenario_service_ontology import ScenarioServiceOntology
from time_series.time_series_service import TimeSeriesService
from time_series.time_series_service_ontology import TimeSeriesServiceOntology


class OntologyServiceFactory(ServiceFactory):
    def get_activity_service(self) -> ActivityService:
        return ActivityServiceOntology()

    def get_activity_execution_service(self) -> ActivityExecutionService:
        return ActivityExecutionServiceOntology()

    def get_appearance_service(self) -> AppearanceService:
        return AppearanceServiceOntology()

    def get_arrangement_service(self) -> ArrangementService:
        return ArrangementServiceOntology()

    def get_channel_service(self) -> ChannelService:
        return ChannelServiceOntology()

    def get_dataset_service(self) -> DatasetService:
        return DatasetServiceOntology()

    def get_experiment_service(self) -> ExperimentService:
        return ExperimentServiceOntology()

    def get_life_activity_service(self) -> LifeActivityService:
        return LifeActivityServiceOntology()

    def get_measure_service(self) -> MeasureService:
        return MeasureServiceOntology()

    def get_measure_name_service(self) -> MeasureNameService:
        return MeasureNameServiceOntology()

    def get_modality_service(self) -> ModalityService:
        return ModalityServiceOntology()

    def get_observable_information_service(self) -> ObservableInformationService:
        return ObservableInformationServiceOntology()

    def get_participant_service(self) -> ParticipantService:
        return ParticipantServiceOntology()

    def get_participant_state_service(self) -> ParticipantStateService:
        return ParticipantStateServiceOntology()

    def get_participation_service(self) -> ParticipationService:
        return ParticipationServiceOntology()

    def get_personality_service(self) -> PersonalityService:
        return PersonalityServiceOntology()

    def get_recording_service(self) -> RecordingService:
        return RecordingServiceOntology()

    def get_registered_channel_service(self) -> RegisteredChannelService:
        return RegisteredChannelServiceOntology()

    def get_registered_data_service(self) -> RegisteredDataService:
        return RegisteredDataServiceOntology()

    def get_scenario_service(self) -> ScenarioService:
        return ScenarioServiceOntology()

    def get_time_series_service(self) -> TimeSeriesService:
        return TimeSeriesServiceOntology()
