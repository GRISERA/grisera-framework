from fastapi import FastAPI

app = FastAPI(title="Ontology API",
              description="Ontology API is reference implementation for creating, manipulating and serialising Ontologies for the GRISERA framework.",
              version="0.1",
              )



@app.get("/", tags=["root"])
async def root():
    """
    Return home page of api
    """
    response = {"title": "Ontology API"}
    response.update({'links': get_links(app)})
    return response

