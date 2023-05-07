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
from life_activity.life_activity_service_graphdb import LifeActivityServiceGraphDB
from measure.measure_service_graphdb import MeasureServiceGraphDB
from measure_name.measure_name_service_graphdb import MeasureNameServiceGraphDB
from modality.modality_service_graphdb import ModalityServiceGraphDB
from participant.participant_service_graphdb import ParticipantServiceGraphDB
from participant_state.participant_state_service_graphdb import (
    ParticipantStateServiceGraphDB,
)
from participation.participation_service_graphdb import ParticipationServiceGraphDB
from personality.personality_service_graphdb import PersonalityServiceGraphDB
from recording.recording_service_mongodb import RecordingServiceMongoDB
from registered_channel.registered_channel_service_mongodb import (
    RegisteredChannelServiceMongoDB,
)
from registered_data.registered_data_service_mongodb import RegisteredDataServiceMongoDB
from scenario.scenario_service_graphdb import ScenarioServiceGraphDB
from time_series.time_series_service_graphdb import TimeSeriesServiceGraphDB
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

        self.channel_service.registered_channel_service = (
            self.registered_channel_service
        )

        self.recording_service.observable_information_service = (
            self.observable_information_service
        )
        self.recording_service.participation_service = None
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
        self.observable_information_service.life_activity_service = None
        self.observable_information_service.modality_service = None
        self.observable_information_service.time_series_service = None

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
        return LifeActivityServiceGraphDB()

    def get_measure_service(self) -> MeasureService:
        return MeasureServiceGraphDB()

    def get_measure_name_service(self) -> MeasureNameService:
        return MeasureNameServiceGraphDB()

    def get_modality_service(self) -> ModalityService:
        return ModalityServiceGraphDB()

    def get_observable_information_service(self) -> ObservableInformationService:
        return self.observable_information_service

    def get_participant_service(self) -> ParticipantService:
        return ParticipantServiceGraphDB()

    def get_participant_state_service(self) -> ParticipantStateService:
        return ParticipantStateServiceGraphDB()

    def get_participation_service(self) -> ParticipationService:
        return ParticipationServiceGraphDB()

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
        return TimeSeriesServiceGraphDB()
