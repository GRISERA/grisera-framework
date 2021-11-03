from activity_execution.activity_execution_router import router as activity_execution_router
from appearance.appearance_router import router as appearance_router
from author.author_router import router as author_router
from channel.channel_router import router as channel_router
from experiment.experiment_router import router as experiment_router
from fastapi import FastAPI
from hateoas import get_links
from live_activity.live_activity_router import router as live_activity_router
from measure.measure_router import router as measure_router
from modality.modality_router import router as modality_router
from observable_information.observable_information_router import router as observable_information_router
from participant.participant_router import router as participant_router
from participant_state.participant_state_router import router as participant_state_router
from participation.participation_router import router as participation_router
from personality.personality_router import router as personality_router
from publication.publication_router import router as publication_router
from recording.recording_router import router as recording_router
from registered_channel.registered_channel_router import router as registered_channel_router
from registered_data.registered_data_router import router as registered_data_router
from scenario.scenario_router import router as scenario_router
from setup import SetupNodes
from time_series.time_series_router import router as time_series_router

app = FastAPI(title="GRISERA API",
              description="Graph Representation Integrating Signals for Emotion Recognition and Analysis (GRISERA) "
                          "framework provides a persistent model for storing integrated signals and methods for its "
                          "creation.",
              version="0.1",
              )
app.include_router(activity_execution_router)
app.include_router(appearance_router)
app.include_router(author_router)
app.include_router(channel_router)
app.include_router(experiment_router)
app.include_router(live_activity_router)
app.include_router(measure_router)
app.include_router(modality_router)
app.include_router(observable_information_router)
app.include_router(participant_router)
app.include_router(participant_state_router)
app.include_router(participation_router)
app.include_router(personality_router)
app.include_router(publication_router)
app.include_router(recording_router)
app.include_router(registered_channel_router)
app.include_router(registered_data_router)
app.include_router(scenario_router)
app.include_router(time_series_router)


@app.on_event("startup")
async def startup_event():
    startup = SetupNodes()
    startup.set_activities()
    startup.set_channels()
    startup.set_arrangements()
    startup.set_modalities()
    startup.set_live_activities()
    startup.set_measure_names()


@app.get("/", tags=["root"])
async def root():
    """
    Return home page of api
    """
    response = {"title": "GRISERA API"}
    response.update({'links': get_links(app)})
    return response
