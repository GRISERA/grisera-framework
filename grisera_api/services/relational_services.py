from services.service_factory import ServiceFactory
from activity.activity_service import ActivityService
from activity.activity_service_relational import ActivityServiceRelational
from activity_execution.activity_execution_service import ActivityExecutionService
from activity_execution.activity_execution_service_relational import  ActivityExecutionServiceRelational
from appearance.appearance_service import AppearanceService
from appearance.appearance_service_relational import AppearanceServiceRelational
from arrangement.arrangement_service import ArrangementService
from arrangement.arrangement_service_relational import ArrangementServiceRelational
from channel.channel_service import ChannelService
from channel.channel_service_relational import ChannelServiceRelational
from experiment.experiment_service import ExperimentService
from experiment.experiment_service_relational import ExperimentServiceRelational
from life_activity.life_activity_service import LifeActivityService
from life_activity.life_activity_service_relational import LifeActivityServiceRelational
from measure.measure_service import MeasureService
from measure.measure_service_relational import MeasureServiceRelational
from measure_name.measure_name_service import MeasureNameService
from measure_name.measure_name_service_relational import MeasureNameServiceRelational
from modality.modality_service import ModalityService
from modality.modality_service_relational import ModalityServiceRelational
from observable_information.observable_information_service import ObservableInformationService
from observable_information.observable_information_service_relational import ObservableInformationServiceRelational
from participant.participant_service import ParticipantService
from participant.participant_service_relational import ParticipantServiceRelational
from participant_state.participant_state_service import ParticipantStateService
from participant_state.participant_state_service_relational import ParticipantStateServiceRelational
from participation.participation_service import ParticipationService
from participation.participation_service_relational import ParticipationServiceRelational
from personality.personality_service import PersonalityService
from personality.personality_service_relational import PersonalityServiceRelational
from recording.recording_service import RecordingService
from recording.recording_service_relational import RecordingServiceRelational
from registered_channel.registered_channel_service import RegisteredChannelService
from registered_channel.registered_channel_service_relational import RegisteredChannelServiceRelational
from registered_data.registered_data_service import RegisteredDataService
from registered_data.registered_data_service_relational import RegisteredDataServiceRelational
from scenario.scenario_service import ScenarioService
from scenario.scenario_service_relational import ScenarioServiceRelational
from time_series.time_series_service import TimeSeriesService
from time_series.time_series_service_relational import TimeSeriesServiceRelational


class RelationalServiceFactory(ServiceFactory):
    def get_activity_service(self) -> ActivityService:
        return ActivityServiceRelational()

    def get_activity_execution_service(self) -> ActivityExecutionService:
        return ActivityExecutionServiceRelational()
    
    def get_appearance_service(self) -> AppearanceService:
        return AppearanceServiceRelational()
    
    def get_arrangement_service(self) -> ArrangementService:
        return ArrangementServiceRelational()
    
    def get_channel_service(self) -> ChannelService:
        return ChannelServiceRelational()
    
    def get_experiment_service(self) -> ExperimentService:
        return ExperimentServiceRelational()
    
    def get_life_activity_service(self) -> LifeActivityService:
        return LifeActivityServiceRelational()
    
    def get_measure_service(self) -> MeasureService:
        return MeasureServiceRelational()
    
    def get_measure_name_service(self) -> MeasureNameService:
        return MeasureNameServiceRelational()
    
    def get_modality_service(self) -> ModalityService:
        return ModalityServiceRelational()
    
    def get_observable_information_service(self) -> ObservableInformationService:
        return ObservableInformationServiceRelational()
    
    def get_participant_service(self) -> ParticipantService:
        return ParticipantServiceRelational()
    
    def get_participant_state_service(self) -> ParticipantStateService:
        return ParticipantStateServiceRelational()
    
    def get_participation_service(self) -> ParticipationService:
        return ParticipationServiceRelational()
    
    def get_personality_service(self) -> PersonalityService:
        return PersonalityServiceRelational()
    
    def get_recording_service(self) -> RecordingService:
        return RecordingServiceRelational()
    
    def get_registered_channel_service(self) -> RegisteredChannelService:
        return RegisteredChannelServiceRelational()
    
    def get_registered_data_service(self) -> RegisteredDataService:
        return RegisteredDataServiceRelational()
    
    def get_scenario_service(self) -> ScenarioService:
        return ScenarioServiceRelational()
    
    def get_time_series_service(self) -> TimeSeriesService:
        return TimeSeriesServiceRelational()
    