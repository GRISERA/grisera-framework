from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from node.node_model import NodeIn, NodeOut
from node.node_service import NodeService
from hateoas import get_links
from typing import List, Dict
from property.property_model import PropertyIn

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

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/nodes", tags=["nodes"], response_model=Dict)
    async def get_nodes(self, label: str, response: Response):
        """
        Get nodes with same label as given
        """
        nodes = self.node_service.get_nodes(label)
        if type(nodes) is dict:
            response.status_code = 422

        get_response = {label: nodes,
                        'links': get_links(router)}

        return get_response

    @router.post("/nodes/{id}/properties", tags=["nodes"], response_model=NodeOut)
    async def create_node_properties(self, id: int, properties: List[PropertyIn], response: Response):
        """
        Create properties for node with given id
        """
        create_response = self.node_service.save_properties(id, properties)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response


