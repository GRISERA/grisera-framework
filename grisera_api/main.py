import os
from time import sleep
from activity.activity_router import router as activity_router, ActivityRouter
from activity_execution.activity_execution_router import router as activity_execution_router
from arrangement.arrangement_router import router as arrangement_router
from appearance.appearance_router import router as appearance_router
from channel.channel_router import router as channel_router
from experiment.experiment_router import router as experiment_router
from fastapi import FastAPI, APIRouter

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
from observable_information.observable_information_service_graphdb import \
    ObservableInformationServiceGraphDB
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
from hateoas import get_links
from life_activity.life_activity_router import router as life_activity_router
from measure.measure_router import router as measure_router
from modality.modality_router import router as modality_router
from observable_information.observable_information_router import router as observable_information_router
from participant.participant_router import router as participant_router
from participant_state.participant_state_router import router as participant_state_router
from participation.participation_router import router as participation_router
from personality.personality_router import router as personality_router
from recording.recording_router import router as recording_router
from registered_channel.registered_channel_router import router as registered_channel_router
from time_series.time_series_router import router as time_series_router, TimeSeriesRouter
from registered_data.registered_data_router import router as registered_data_router
from scenario.scenario_router import router as scenario_router
from measure_name.measure_name_router import router as measure_name_router
from setup import SetupNodes
from graph_api_config import *

app = FastAPI(title="GRISERA API",
              description="Graph Representation Integrating Signals for Emotion Recognition and Analysis (GRISERA) "
                          "framework provides a persistent model for storing integrated signals and methods for its "
                          "creation.",
              version="0.1",
              )
app.include_router(activity_router)
app.include_router(activity_execution_router)
app.include_router(appearance_router)
app.include_router(arrangement_router)
app.include_router(channel_router)
app.include_router(experiment_router)
app.include_router(life_activity_router)
app.include_router(measure_router)
app.include_router(measure_name_router)
app.include_router(modality_router)
app.include_router(observable_information_router)
app.include_router(participant_router)
app.include_router(participant_state_router)
app.include_router(participation_router)
app.include_router(personality_router)
app.include_router(recording_router)
app.include_router(registered_channel_router)
app.include_router(registered_data_router)
app.include_router(scenario_router)
app.include_router(time_series_router)


@app.on_event("startup")
async def startup_event():
    startup = SetupNodes()
    sleep(40)
    if not os.path.exists("lock"):
        open("lock", "w").write("Busy")
        sleep(40)
        startup.set_activities()
        startup.set_channels()
        startup.set_arrangements()
        startup.set_modalities()
        startup.set_life_activities()
        startup.set_measure_names()
        os.remove("lock")


@app.get("/", tags=["root"])
async def root():
    """
    Return home page of api
    """
    response = {"title": "GRISERA API"}
    response.update({'links': get_links(app)})
    return response
