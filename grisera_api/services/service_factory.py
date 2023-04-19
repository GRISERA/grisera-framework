from abc import ABC, abstractmethod

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

class ServiceFactory(ABC):    

    @abstractmethod
    def get_activity_service(self) -> ActivityService:
        pass

    @abstractmethod
    def get_activity_execution_service(self) -> ActivityExecutionService:
        pass

    @abstractmethod
    def get_appearance_service(self) -> AppearanceService:
        pass

    @abstractmethod
    def get_arrangement_service(self) -> ArrangementService:
        pass

    @abstractmethod
    def get_channel_service(self) -> ChannelService:
        pass

    @abstractmethod
    def get_experiment_service(self) -> ExperimentService:
        pass

    @abstractmethod
    def get_life_activity_service(self) -> LifeActivityService:
        pass

    @abstractmethod
    def get_measure_service(self) -> MeasureService:
        pass

    @abstractmethod
    def get_measure_name_service(self) -> MeasureNameService:
        pass

    @abstractmethod
    def get_modality_service(self) -> ModalityService:
        pass

    @abstractmethod
    def get_observable_information_service(self) -> ObservableInformationService:
        pass

    @abstractmethod
    def get_participant_service(self) -> ParticipantService:
        pass

    @abstractmethod
    def get_participant_state_service(self) -> ParticipantStateService:
        pass

    @abstractmethod
    def get_participation_service(self) -> ParticipationService:
        pass

    @abstractmethod
    def get_personality_service(self) -> PersonalityService:
        pass

    @abstractmethod
    def get_recording_service(self) -> RecordingService:
        pass

    @abstractmethod
    def get_registered_channel_service(self) -> RegisteredChannelService:
        pass

    @abstractmethod
    def get_registered_data_service(self) -> RegisteredDataService:
        pass

    @abstractmethod
    def get_scenario_service(self) -> ScenarioService:
        pass

    @abstractmethod
    def get_time_series_service(self) -> TimeSeriesService:
        pass