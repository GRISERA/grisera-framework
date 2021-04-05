from fastapi import FastAPI
from .node.node_router import router


app = FastAPI()

app.include_router(router)


@app.get("/", tags=["root"])
async def root():
    """
    Return home page of api
    """
    return {"title": "Graph DB API"}


