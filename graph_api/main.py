from fastapi import FastAPI
from node.node_router import router as node_router
from relationship.relationship_router import router as relationship_router
from hateoas import get_links

app = FastAPI()

app.include_router(node_router)
app.include_router(relationship_router)


@app.get("/", tags=["root"])
async def root():
    """
    Return home page of api
    """
    response = {"title": "Graph DB API"}
    response.update({'links': get_links(app)})
    return response
