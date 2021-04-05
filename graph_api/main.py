from fastapi import FastAPI
from .node.node_router import router
from .hateoas import get_links

app = FastAPI()

app.include_router(router)


@app.get("/", tags=["root"])
async def root():
    """
    Return home page of api
    """
    response = {"title": "Graph DB API"}
    response.update({'links': get_links(app)})
    return response

