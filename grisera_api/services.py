import os
from enum import Enum

from activity.activity_service import ActivityService
from activity.activity_service_graphdb import ActivityServiceGraphDB
from activity.activity_service_ontology import ActivityServiceOntology
from activity_execution.activity_execution_service import ActivityExecutionService
from activity_execution.activity_execution_service_graphdb import ActivityExecutionServiceGraphDB
from activity_execution.activity_execution_service_ontology import ActivityExecutionServiceOntology
from appearance.appearance_service import AppearanceService
from appearance.appearance_service_graphdb import AppearanceServiceGraphDB
from appearance.appearance_service_ontology import AppearanceServiceOntology
from arrangement.arrangement_service import ArrangementService
from arrangement.arrangement_service_graphdb import ArrangementServiceGraphDB
from arrangement.arrangement_service_ontology import ArrangementServiceOntology
from channel.channel_service import ChannelService
from channel.channel_service_graphdb import ChannelServiceGraphDB
from channel.channel_service_ontology import ChannelServiceOntology
from experiment.experiment_service import ExperimentService
from experiment.experiment_service_graphdb import ExperimentServiceGraphDB
from experiment.experiment_service_ontology import ExperimentServiceOntology
from life_activity.life_activity_service import LifeActivityService
from life_activity.life_activity_service_graphdb import LifeActivityServiceGraphDB
from life_activity.life_activity_service_ontology import LifeActivityServiceOntology
from measure.measure_service import MeasureService
from measure.measure_service_graphdb import MeasureServiceGraphDB
from measure.measure_service_ontology import MeasureServiceOntology
from measure_name.measure_name_service import MeasureNameService
from measure_name.measure_name_service_graphdb import MeasureNameServiceGraphDB
from measure_name.measure_name_service_ontology import MeasureNameServiceOntology
from modality.modality_service import ModalityService
from modality.modality_service_graphdb import ModalityServiceGraphDB
from modality.modality_service_ontology import ModalityServiceOntology
from observable_information.observable_information_service import ObservableInformationService
from observable_information.observable_information_service_graphdb import ObservableInformationServiceGraphDB
from observable_information.observable_information_service_ontology import ObservableInformationServiceOntology
from participant.participant_service import ParticipantService
from participant.participant_service_graphdb import ParticipantServiceGraphDB
from participant.participant_service_ontology import ParticipantServiceOntology
from participant_state.participant_state_service import ParticipantStateService
from participant_state.participant_state_service_graphdb import ParticipantStateServiceGraphDB
from participant_state.participant_state_service_ontology import ParticipantStateServiceOntology
from participation.participation_service import ParticipationService
from participation.participation_service_graphdb import ParticipationServiceGraphDB
from participation.participation_service_ontology import ParticipationServiceOntology
from personality.personality_service import PersonalityService
from personality.personality_service_graphdb import PersonalityServiceGraphDB
from personality.personality_service_ontology import PersonalityServiceOntology
from recording.recording_service import RecordingService
from recording.recording_service_graphdb import RecordingServiceGraphDB
from recording.recording_service_ontology import RecordingServiceOntology
from registered_channel.registered_channel_service import RegisteredChannelService
from registered_channel.registered_channel_service_graphdb import RegisteredChannelServiceGraphDB
from registered_channel.registered_channel_service_ontology import RegisteredChannelServiceOntology
from registered_data.registered_data_service import RegisteredDataService
from registered_data.registered_data_service_graphdb import RegisteredDataServiceGraphDB
from registered_data.registered_data_service_ontology import RegisteredDataServiceOntology
from scenario.scenario_service import ScenarioService
from scenario.scenario_service_graphdb import ScenarioServiceGraphDB
from scenario.scenario_service_ontology import ScenarioServiceOntology
from time_series.time_series_service import TimeSeriesService
from time_series.time_series_service_graphdb import TimeSeriesServiceGraphDB
from time_series.time_series_service_graphdb_with_signal_values import TimeSeriesServiceGraphDBWithSignalValues
from time_series.time_series_service_ontology import TimeSeriesServiceOntology


class PersistenceTypes(Enum):
    GRAPHDB = 1
    ONTOLOGY = 2
    GRAPHDB_WITH_SIGNAL_VALUES = 3


class Services:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Services, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.persistence_type = PersistenceTypes(
            int(os.environ.get('PERSISTENCE_TYPE'))) if 'PERSISTENCE_TYPE' in os.environ else PersistenceTypes.GRAPHDB

    def activity_service(self) -> ActivityService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return ActivityServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return ActivityServiceOntology()
        else:
            return ActivityService()

    def activity_execution_service(self) -> ActivityExecutionService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return ActivityExecutionServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return ActivityExecutionServiceOntology()
        else:
            return ActivityExecutionService()

    def appearance_service(self) -> AppearanceService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return AppearanceServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return AppearanceServiceOntology()
        else:
            return AppearanceService()

    def arrangement_service(self) -> ArrangementService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return ArrangementServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return ArrangementServiceOntology()
        else:
            return ArrangementService()

    def channel_service(self) -> ChannelService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return ChannelServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return ChannelServiceOntology()
        else:
            return ChannelService()

    def experiment_service(self) -> ExperimentService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return ExperimentServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return ExperimentServiceOntology()
        else:
            return ExperimentService()

    def life_activity_service(self) -> LifeActivityService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return LifeActivityServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return LifeActivityServiceOntology()
        else:
            return LifeActivityService()

    def measure_service(self) -> MeasureService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return MeasureServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return MeasureServiceOntology()
        else:
            return MeasureService()

    def measure_name_service(self) -> MeasureNameService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return MeasureNameServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return MeasureNameServiceOntology()
        else:
            return MeasureNameService()

    def modality_service(self) -> ModalityService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return ModalityServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return ModalityServiceOntology()
        else:
            return ModalityService()

    def observable_information_service(self) -> ObservableInformationService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return ObservableInformationServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return ObservableInformationServiceOntology()
        else:
            return ObservableInformationService()

    def participant_service(self) -> ParticipantService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return ParticipantServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return ParticipantServiceOntology()
        else:
            return ParticipantService()

    def participant_state_service(self) -> ParticipantStateService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return ParticipantStateServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return ParticipantStateServiceOntology()
        else:
            return ParticipantStateService()

    def participation_service(self) -> ParticipationService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return ParticipationServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return ParticipationServiceOntology()
        else:
            return ParticipationService()

    def personality_service(self) -> PersonalityService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return PersonalityServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return PersonalityServiceOntology()
        else:
            return PersonalityService()

    def recording_service(self) -> RecordingService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return RecordingServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return RecordingServiceOntology()
        else:
            return RecordingService()

    def registered_channel_service(self) -> RegisteredChannelService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return RegisteredChannelServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return RegisteredChannelServiceOntology()
        else:
            return RegisteredChannelService()

    def registered_data_service(self) -> RegisteredDataService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return RegisteredDataServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return RegisteredDataServiceOntology()
        else:
            return RegisteredDataService()

    def scenario_service(self) -> ScenarioService:
        if self.persistence_type in [PersistenceTypes.GRAPHDB, PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES]:
            return ScenarioServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return ScenarioServiceOntology()
        else:
            return ScenarioService()

    def time_series_service(self) -> TimeSeriesService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return TimeSeriesServiceGraphDB()
        elif self.persistence_type == PersistenceTypes.GRAPHDB_WITH_SIGNAL_VALUES:
            return TimeSeriesServiceGraphDBWithSignalValues()
        elif self.persistence_type == PersistenceTypes.ONTOLOGY:
            return TimeSeriesServiceOntology()
        else:
            return TimeSeriesService()
