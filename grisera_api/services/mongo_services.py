from observable_information.observable_information_service_mongodb import (
    ObservableInformationServiceMongoDB,
)
from services.service_factory import ServiceFactory
from activity.activity_service_graphdb import ActivityServiceGraphDB
from activity_execution.activity_execution_service_graphdb import (
    ActivityExecutionServiceGraphDB,
)
from appearance.appearance_service_graphdb import AppearanceServiceGraphDB
from arrangement.arrangement_service_graphdb import ArrangementServiceGraphDB
from channel.channel_service_mongodb import ChannelServiceMongoDB
from experiment.experiment_service_graphdb import ExperimentServiceGraphDB
from life_activity.life_activity_service_mongodb import LifeActivityServiceMongoDB
from measure.measure_service_mongodb import MeasureServiceMongoDB
from measure_name.measure_name_service_mongodb import MeasureNameServiceMongoDB
from modality.modality_service_mongodb import ModalityServiceMongoDB
from participant.participant_service_mongodb import ParticipantServiceMongoDB
from participant_state.participant_state_service_mongodb import (
    ParticipantStateServiceMongoDB,
)
from participation.participation_service_mongodb import ParticipationServiceMongoDB
from personality.personality_service_graphdb import PersonalityServiceGraphDB
from recording.recording_service_mongodb import RecordingServiceMongoDB
from registered_channel.registered_channel_service_mongodb import (
    RegisteredChannelServiceMongoDB,
)
from registered_data.registered_data_service_mongodb import RegisteredDataServiceMongoDB
from scenario.scenario_service_graphdb import ScenarioServiceGraphDB
from time_series.time_series_service_mongodb import TimeSeriesServiceMongoDB
from activity.activity_service import ActivityService
from activity_execution.activity_execution_service import ActivityExecutionService
from appearance.appearance_service import AppearanceService
from arrangement.arrangement_service import ArrangementService
from channel.channel_service import ChannelService
from experiment.experiment_service import ExperimentService
from life_activity.life_activity_service import LifeActivityService
from measure.measure_service import MeasureService
from measure_name.measure_name_service import MeasureNameService
from modality.modality_service import ModalityService
from observable_information.observable_information_service import (
    ObservableInformationService,
)
from participant.participant_service import ParticipantService
from participant_state.participant_state_service import ParticipantStateService
from participation.participation_service import ParticipationService
from personality.personality_service import PersonalityService
from recording.recording_service import RecordingService
from registered_channel.registered_channel_service import RegisteredChannelService
from registered_data.registered_data_service import RegisteredDataService
from scenario.scenario_service import ScenarioService
from time_series.time_series_service import TimeSeriesService


class MongoServiceFactory(ServiceFactory):
    def __init__(self):
        self.channel_service = ChannelServiceMongoDB()
        self.recording_service = RecordingServiceMongoDB()
        self.registered_channel_service = RegisteredChannelServiceMongoDB()
        self.registered_data_service = RegisteredDataServiceMongoDB()
        self.observable_information_service = ObservableInformationServiceMongoDB()
        self.modality_service = ModalityServiceMongoDB()
        self.life_activity_service = LifeActivityServiceMongoDB()
        self.time_series_service = TimeSeriesServiceMongoDB()
        self.measure_service = MeasureServiceMongoDB()
        self.measure_name_service = MeasureNameServiceMongoDB()
        self.participation_service = ParticipationServiceMongoDB()
        self.participant_service = ParticipantService()
        self.participant_state_service = ParticipantStateService()

        self.channel_service.registered_channel_service = (
            self.registered_channel_service
        )

        self.recording_service.observable_information_service = (
            self.observable_information_service
        )
        self.recording_service.participation_service = self.participation_service
        self.recording_service.registered_channel_service = (
            self.registered_channel_service
        )

        self.registered_channel_service.channel_service = self.channel_service
        self.registered_channel_service.registered_data_service = (
            self.registered_data_service
        )
        self.registered_channel_service.recording_service = self.recording_service

        self.registered_data_service.registered_channel_service = (
            self.registered_channel_service
        )

        self.observable_information_service.recording_service = self.recording_service
        self.observable_information_service.life_activity_service = (
            self.life_activity_service
        )
        self.observable_information_service.modality_service = self.modality_service
        self.observable_information_service.time_series_service = (
            self.time_series_service
        )

        self.modality_service.observable_information_service = (
            self.observable_information_service
        )

        self.life_activity_service.observable_information_service = (
            self.observable_information_service
        )

        self.time_series_service.observable_information_service = (
            self.observable_information_service
        )
        self.time_series_service.measure_service = self.measure_service

        self.measure_service.time_series_service = self.time_series_service
        self.measure_service.measure_name_service = self.measure_name_service

        self.measure_name_service.measure_service = self.measure_service

        self.participation_service.recording_service = self.recording_service
        self.participation_service.activity_execution_service = None
        self.participation_service.participant_state_service = (
            self.participant_state_service
        )

        self.participant_service.participant_state_service = (
            self.participant_state_service
        )

        self.participant_state_service.participant_service = self.participant_service
        self.participant_state_service.appearance_service = None
        self.participant_state_service.personality_service = None
        self.participant_state_service.participation_service = (
            self.participation_service
        )

    def get_activity_service(self) -> ActivityService:
        return ActivityServiceGraphDB()

    def get_activity_execution_service(self) -> ActivityExecutionService:
        return ActivityExecutionServiceGraphDB()

    def get_appearance_service(self) -> AppearanceService:
        return AppearanceServiceGraphDB()

    def get_arrangement_service(self) -> ArrangementService:
        return ArrangementServiceGraphDB()

    def get_channel_service(self) -> ChannelService:
        return self.channel_service

    def get_experiment_service(self) -> ExperimentService:
        return ExperimentServiceGraphDB()

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
        return PersonalityServiceGraphDB()

    def get_recording_service(self) -> RecordingService:
        return self.recording_service

    def get_registered_channel_service(self) -> RegisteredChannelService:
        return self.registered_channel_service

    def get_registered_data_service(self) -> RegisteredDataService:
        return self.registered_data_service

    def get_scenario_service(self) -> ScenarioService:
        return ScenarioServiceGraphDB()

    def get_time_series_service(self) -> TimeSeriesService:
        return self.time_series_service
