from fastapi import FastAPI
from hateoas import get_links
from participant.participant_router import router as participant_router
from experiment.experiment_router import router as experiment_router
from publication.publication_router import router as publication_router
from author.author_router import router as author_router
from scenario.scenario_router import router as scenario_router
from activity.activity_router import router as activity_router
from observable_information.observable_information_router import router as observable_information_router
from participant_state.participant_state_router import router as participant_state_router


app = FastAPI(title="GRISERA API",
              description="Graph Representation Integrating Signals for Emotion Recognition and Analysis (GRISERA) "
                          "framework provides a persistent model for storing integrated signals and methods for its "
                          "creation.",
              version="0.1",
              )
app.include_router(participant_router)
app.include_router(experiment_router)
app.include_router(author_router)
app.include_router(publication_router)
app.include_router(activity_router)
app.include_router(scenario_router)
app.include_router(observable_information_router)
app.include_router(participant_state_router)


@app.get("/", tags=["root"])
async def root():
    """
    Return home page of api
    """
    response = {"title": "GRISERA API"}
    response.update({'links': get_links(app)})
    return response
