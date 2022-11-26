import os
from enum import Enum

from activity.activity_service import ActivityService
from activity.activity_service_graphdb import ActivityServiceGraphDB
from activity_execution.activity_execution_service import ActivityExecutionService
from activity_execution.activity_execution_service_graphdb import ActivityExecutionServiceGraphDB
from appearance.appearance_service import AppearanceService
from appearance.appearance_service_graphdb import AppearanceServiceGraphDB
from arrangement.arrangement_service import ArrangementService
from arrangement.arrangement_service_graphdb import ArrangementServiceGraphDB
from channel.channel_service import ChannelService
from channel.channel_service_graphdb import ChannelServiceGraphDB
from experiment.experiment_service import ExperimentService
from experiment.experiment_service_graphdb import ExperimentServiceGraphDB
from life_activity.life_activity_service import LifeActivityService
from life_activity.life_activity_service_graphdb import LifeActivityServiceGraphDB
from measure.measure_service import MeasureService
from measure.measure_service_graphdb import MeasureServiceGraphDB
from measure_name.measure_name_service import MeasureNameService
from measure_name.measure_name_service_graphdb import MeasureNameServiceGraphDB
from modality.modality_service import ModalityService
from modality.modality_service_graphdb import ModalityServiceGraphDB
from observable_information.observable_information_service import ObservableInformationService
from observable_information.observable_information_service_graphdb import ObservableInformationServiceGraphDB
from participant.participant_service import ParticipantService
from participant.participant_service_graphdb import ParticipantServiceGraphDB
from participant_state.participant_state_service import ParticipantStateService
from participant_state.participant_state_service_graphdb import ParticipantStateServiceGraphDB
from participation.participation_service import ParticipationService
from participation.participation_service_graphdb import ParticipationServiceGraphDB
from personality.personality_service import PersonalityService
from personality.personality_service_graphdb import PersonalityServiceGraphDB
from recording.recording_service import RecordingService
from recording.recording_service_graphdb import RecordingServiceGraphDB
from registered_channel.registered_channel_service import RegisteredChannelService
from registered_channel.registered_channel_service_graphdb import RegisteredChannelServiceGraphDB
from registered_data.registered_data_service import RegisteredDataService
from registered_data.registered_data_service_graphdb import RegisteredDataServiceGraphDB
from scenario.scenario_service import ScenarioService
from scenario.scenario_service_graphdb import ScenarioServiceGraphDB
from time_series.time_series_service import TimeSeriesService
from time_series.time_series_service_graphdb import TimeSeriesServiceGraphDB


class PersistenceTypes(Enum):
    GRAPHDB = 1
    ONTOLOGY = 2


class Services:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Services, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.persistence_type = os.environ.get('PERSISTENCE_TYPE') or PersistenceTypes.GRAPHDB

    def activity_service(self) -> ActivityService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return ActivityServiceGraphDB()
        else:
            return ActivityService

    def activity_execution_service(self) -> ActivityExecutionService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return ActivityExecutionServiceGraphDB()
        else:
            return ActivityExecutionService

    def appearance_service(self) -> AppearanceService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return AppearanceServiceGraphDB()
        else:
            return AppearanceService

    def arrangement_service(self) -> ArrangementService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return ArrangementServiceGraphDB()
        else:
            return ArrangementService

    def channel_service(self) -> ChannelService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return ChannelServiceGraphDB()
        else:
            return ChannelService

    def experiment_service(self) -> ExperimentService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return ExperimentServiceGraphDB()
        else:
            return ExperimentService

    def life_activity_service(self) -> LifeActivityService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return LifeActivityServiceGraphDB()
        else:
            return LifeActivityService

    def measure_service(self) -> MeasureService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return MeasureServiceGraphDB()
        else:
            return MeasureService

    def measure_name_service(self) -> MeasureNameService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return MeasureNameServiceGraphDB()
        else:
            return MeasureNameService

    def modality_service(self) -> ModalityService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return ModalityServiceGraphDB()
        else:
            return ModalityService

    def observable_information_service(self) -> ObservableInformationService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return ObservableInformationServiceGraphDB()
        else:
            return ObservableInformationService

    def participant_service(self) -> ParticipantService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return ParticipantServiceGraphDB()
        else:
            return ParticipantService

    def participant_state_service(self) -> ParticipantStateService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return ParticipantStateServiceGraphDB()
        else:
            return ParticipantStateService

    def participation_service(self) -> ParticipationService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return ParticipationServiceGraphDB()
        else:
            return ParticipationService

    def personality_service(self) -> PersonalityService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return PersonalityServiceGraphDB()
        else:
            return PersonalityService

    def recording_service(self) -> RecordingService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return RecordingServiceGraphDB()
        else:
            return RecordingService

    def registered_channel_service(self) -> RegisteredChannelService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return ParticipationServiceGraphDB()
        else:
            return ParticipationService

    def registered_data_service(self) -> RegisteredDataService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return RegisteredDataServiceGraphDB()
        else:
            return RegisteredDataService

    def scenario_service(self) -> ScenarioService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return ScenarioServiceGraphDB()
        else:
            return ScenarioService

    def time_series_service(self) -> TimeSeriesService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return TimeSeriesServiceGraphDB()
        else:
            return TimeSeriesService
