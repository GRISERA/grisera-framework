import os
from enum import Enum
from services.mongo_services import MongoServiceFactory

from services.service_factory import ServiceFactory
from services.graph_services import (
    GraphServiceFactory,
    GraphWithSignalValuesServiceFactory,
)
from services.ontology_services import OntologyServiceFactory
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


class PersistenceTypes(Enum):
    GRAPHDB = 1
    ONTOLOGY = 2
    GRAPHDB_WITH_SIGNAL_VALUES = 3
    MONGODB = 4


class Services:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Services, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.persistence_type = (
            PersistenceTypes(int(os.environ.get("PERSISTENCE_TYPE")))
            if "PERSISTENCE_TYPE" in os.environ
            else PersistenceTypes.GRAPHDB
        )
        self.service_factory = self.get_service_factory()

    def get_service_factory(self) -> ServiceFactory:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return GraphServiceFactory()
        elif self.persistence_type == PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES:
            return GraphWithSignalValuesServiceFactory()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return OntologyServiceFactory()
        elif self.persistence_type == PersistenceTypes.MONGODB:
            return MongoServiceFactory()
        else:
            return ServiceFactory()

    def activity_service(self) -> ActivityService:
        return self.service_factory.get_activity_service()

    def activity_execution_service(self) -> ActivityExecutionService:
        return self.service_factory.get_activity_execution_service()

    def appearance_service(self) -> AppearanceService:
        return self.service_factory.get_appearance_service()

    def arrangement_service(self) -> ArrangementService:
        return self.service_factory.get_arrangement_service()

    def channel_service(self) -> ChannelService:
        return self.service_factory.get_channel_service()

    def experiment_service(self) -> ExperimentService:
        return self.service_factory.get_experiment_service()

    def life_activity_service(self) -> LifeActivityService:
        return self.service_factory.get_life_activity_service()

    def measure_service(self) -> MeasureService:
        return self.service_factory.get_measure_service()

    def measure_name_service(self) -> MeasureNameService:
        return self.service_factory.get_measure_name_service()

    def modality_service(self) -> ModalityService:
        return self.service_factory.get_modality_service()

    def observable_information_service(self) -> ObservableInformationService:
        return self.service_factory.get_observable_information_service()

    def participant_service(self) -> ParticipantService:
        return self.service_factory.get_participant_service()

    def participant_state_service(self) -> ParticipantStateService:
        return self.service_factory.get_participant_state_service()

    def participation_service(self) -> ParticipationService:
        return self.service_factory.get_participation_service()

    def personality_service(self) -> PersonalityService:
        return self.service_factory.get_personality_service()

    def recording_service(self) -> RecordingService:
        return self.service_factory.get_recording_service()

    def registered_channel_service(self) -> RegisteredChannelService:
        return self.service_factory.get_registered_channel_service()

    def registered_data_service(self) -> RegisteredDataService:
        return self.service_factory.get_registered_data_service()

    def scenario_service(self) -> ScenarioService:
        return self.service_factory.get_scenario_service()

    def time_series_service(self) -> TimeSeriesService:
        return self.service_factory.get_time_series_service()
