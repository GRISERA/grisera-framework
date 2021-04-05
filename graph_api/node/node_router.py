from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from .node_model import NodeIn, NodeOut
from .node_service import NodeService

router = InferringRouter()


@cbv(router)
class NodeRouter:
    """
    Class for routing node based requests

    Attributes:
        node_service (NodeService): Service instance for nodes
    """
    node_service = NodeService()

    @router.post("/nodes", tags=["nodes"], response_model=NodeOut)
    async def create_node(self, node: NodeIn, response: Response):
        """
        Create node with optional labels
        """
        create_response = self.node_service.save_node(node)

        if create_response.errors is not None:
            response.status_code = 422

        return create_response
