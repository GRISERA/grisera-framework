from services.service_factory import ServiceFactory
from activity.activity_service_graphdb import ActivityServiceGraphDB
from activity_execution.activity_execution_service_graphdb import ActivityExecutionServiceGraphDB
from appearance.appearance_service_graphdb import AppearanceServiceGraphDB
from arrangement.arrangement_service_graphdb import ArrangementServiceGraphDB
from channel.channel_service_graphdb import ChannelServiceGraphDB
from dataset.dataset_service_graphdb import DatasetServiceGraphDB
from experiment.experiment_service_graphdb import ExperimentServiceGraphDB
from life_activity.life_activity_service_graphdb import LifeActivityServiceGraphDB
from measure.measure_service_graphdb import MeasureServiceGraphDB
from measure_name.measure_name_service_graphdb import MeasureNameServiceGraphDB
from modality.modality_service_graphdb import ModalityServiceGraphDB
from observable_information.observable_information_service_graphdb import ObservableInformationServiceGraphDB
from participant.participant_service_graphdb import ParticipantServiceGraphDB
from participant_state.participant_state_service_graphdb import ParticipantStateServiceGraphDB
from participation.participation_service_graphdb import ParticipationServiceGraphDB
from personality.personality_service_graphdb import PersonalityServiceGraphDB
from recording.recording_service_graphdb import RecordingServiceGraphDB
from registered_channel.registered_channel_service_graphdb import RegisteredChannelServiceGraphDB
from registered_data.registered_data_service_graphdb import RegisteredDataServiceGraphDB
from scenario.scenario_service_graphdb import ScenarioServiceGraphDB
from time_series.time_series_service_graphdb import TimeSeriesServiceGraphDB
from activity.activity_service import ActivityService
from activity_execution.activity_execution_service import ActivityExecutionService
from appearance.appearance_service import AppearanceService
from arrangement.arrangement_service import ArrangementService
from channel.channel_service import ChannelService
from dataset.dataset_service import DatasetService
from experiment.experiment_service import ExperimentService
from life_activity.life_activity_service import LifeActivityService
from measure.measure_service import MeasureService
from measure_name.measure_name_service import MeasureNameService
from modality.modality_service import ModalityService
from observable_information.observable_information_service import ObservableInformationService
from participant.participant_service import ParticipantService
from participant_state.participant_state_service import ParticipantStateService
from participation.participation_service import ParticipationService
from personality.personality_service import PersonalityService
from recording.recording_service import RecordingService
from registered_channel.registered_channel_service import RegisteredChannelService
from registered_data.registered_data_service import RegisteredDataService
from scenario.scenario_service import ScenarioService
from time_series.time_series_service import TimeSeriesService
from time_series.time_series_service_graphdb_with_signal_values import TimeSeriesServiceGraphDBWithSignalValues


class GraphServiceFactory(ServiceFactory):
    def __init__(self):
        self.activity_service = ActivityServiceGraphDB()
        self.activity_execution_service = ActivityExecutionServiceGraphDB()
        self.appearance_service = AppearanceServiceGraphDB()
        self.arrangement_service = ArrangementServiceGraphDB()
        self.channel_service = ChannelServiceGraphDB()
        self.dataset_service = DatasetServiceGraphDB()
        self.experiment_service = ExperimentServiceGraphDB()
        self.life_activity_service = LifeActivityServiceGraphDB()
        self.measure_service = MeasureServiceGraphDB()
        self.measure_name_service = MeasureNameServiceGraphDB()
        self.modality_service = ModalityServiceGraphDB()
        self.observable_information_service = ObservableInformationServiceGraphDB()
        self.participant_service = ParticipantServiceGraphDB()
        self.participant_state_service = ParticipantStateServiceGraphDB()
        self.participation_service = ParticipationServiceGraphDB()
        self.personality_service = PersonalityServiceGraphDB()
        self.recording_service = RecordingServiceGraphDB()
        self.registered_channel_service = RegisteredChannelServiceGraphDB()
        self.registered_data_service = RegisteredDataServiceGraphDB()
        self.scenario_service = ScenarioServiceGraphDB()
        self.time_series_service = TimeSeriesServiceGraphDB()
        self.time_series_with_signal_values_service = TimeSeriesServiceGraphDBWithSignalValues()

        self.activity_service.activity_execution_service = self.activity_execution_service

        self.activity_execution_service.activity_service = self.activity_execution_service
        self.activity_execution_service.arrangement_service = self.arrangement_service
        self.activity_execution_service.scenario_service = self.scenario_service
        self.activity_execution_service.experiment_service = self.experiment_service
        self.activity_execution_service.participation_service = self.participation_service

        self.appearance_service.participant_state_service = self.participant_state_service

        self.arrangement_service.activity_execution_service = self.activity_execution_service

        self.channel_service.registered_channel_service = self.registered_channel_service

        self.dataset_service.dataset_service = self.dataset_service

        self.experiment_service.activity_execution_service = self.activity_execution_service

        self.life_activity_service.observable_information_service = self.observable_information_service

        self.measure_service.measure_name_service = self.measure_name_service
        self.measure_service.time_series_service = self.time_series_service

        self.measure_name_service.measure_service = self.measure_service

        self.modality_service.observable_information_service = self.observable_information_service

        self.observable_information_service.modality_service = self.modality_service
        self.observable_information_service.recording_service = self.recording_service
        self.observable_information_service.life_activity_service = self.life_activity_service
        self.observable_information_service.time_series_service = self.time_series_service

        self.participant_service.participant_state_service = self.participant_state_service

        self.participant_state_service.participant_service = self.participant_service
        self.participant_state_service.participation_service = self.participation_service
        self.participant_state_service.appearance_service = self.appearance_service
        self.participant_state_service.personality_service = self.personality_service

        self.participation_service.participant_state_service = self.participant_state_service
        self.participation_service.recording_service = self.recording_service
        self.participation_service.activity_execution_service = self.activity_execution_service

        self.personality_service.participant_state_service = self.participant_state_service

        self.recording_service.participation_service = self.participation_service
        self.recording_service.registered_channel_service = self.registered_channel_service
        self.recording_service.observable_information_service = self.observable_information_service

        self.registered_channel_service.recording_service = self.recording_service
        self.registered_channel_service.channel_service = self.channel_service
        self.registered_channel_service.registered_data_service = self.registered_data_service

        self.registered_data_service.registered_channel_service = self.registered_channel_service

        self.scenario_service.experiment_service = self.experiment_service
        self.scenario_service.activity_execution_service = self.activity_execution_service

        self.time_series_service.measure_service = self.measure_service
        self.time_series_service.observable_information_service = self.observable_information_service

        self.time_series_with_signal_values_service.measure_service = self.measure_service
        self.time_series_with_signal_values_service.observable_information_service = self.observable_information_service

    def get_activity_service(self) -> ActivityService:
        return self.activity_service

    def get_activity_execution_service(self) -> ActivityExecutionService:
        return self.activity_execution_service

    def get_appearance_service(self) -> AppearanceService:
        return self.appearance_service

    def get_arrangement_service(self) -> ArrangementService:
        return self.arrangement_service

    def get_channel_service(self) -> ChannelService:
        return self.channel_service

    def get_dataset_service(self) -> DatasetService:
        return self.dataset_service

    def get_experiment_service(self) -> ExperimentService:
        return self.experiment_service

    def get_life_activity_service(self) -> LifeActivityService:
        return self.life_activity_service

    def get_measure_service(self) -> MeasureService:
        return self.measure_service

    def get_measure_name_service(self) -> MeasureNameService:
        return self.measure_name_service

    def get_modality_service(self) -> ModalityService:
        return self.modality_service

    def get_observable_information_service(self) -> ObservableInformationService:
        return self.observable_information_service

    def get_participant_service(self) -> ParticipantService:
        return self.participant_service

    def get_participant_state_service(self) -> ParticipantStateService:
        return self.participant_state_service

    def get_participation_service(self) -> ParticipationService:
        return self.participation_service

    def get_personality_service(self) -> PersonalityService:
        return self.personality_service

    def get_recording_service(self) -> RecordingService:
        return self.recording_service

    def get_registered_channel_service(self) -> RegisteredChannelService:
        return self.registered_channel_service

    def get_registered_data_service(self) -> RegisteredDataService:
        return self.registered_data_service

    def get_scenario_service(self) -> ScenarioService:
        return self.scenario_service

    def get_time_series_service(self) -> TimeSeriesService:
        return self.time_series_service


class GraphWithSignalValuesServiceFactory(GraphServiceFactory):
    def get_time_series_service(self) -> TimeSeriesService:
        return self.time_series_with_signal_values_service
