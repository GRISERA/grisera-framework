from fastapi import FastAPI
from hateoas import get_links
from model.model_router import router as model_router
from instance.instance_router import router as instance_router
app = FastAPI(title="Ontology API",
              description="Ontology API is reference implementation for creating, manipulating and serialising Ontologies for the GRISERA framework.",
              version="0.1",
              )

app.include_router(model_router)
app.include_router(instance_router)

@app.get("/", tags=["root"])
async def root():
    """
    Return home page of api
    """
    response = {"title": "Ontology API"}
    response.update({'links': get_links(app)})
    return response