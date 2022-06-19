from fastapi import Query, Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from node.node_model import NodeIn, NodeOut, NodesOut
from node.node_service import NodeService
from hateoas import get_links
from typing import List, Union
from property.property_model import PropertyIn
from relationship.relationship_model import RelationshipsOut
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

    @router.get("/nodes/{id}", tags=["nodes"], response_model=NodeOut)
    async def get_node(self, id: int, response: Response):
        """
        Get node with same id as given
        """
        node = self.node_service.get_node(id)
        if node.errors is not None:
            response.status_code = 404

        node.links = get_links(router)

        return node

    @router.get("/nodes", tags=["nodes"], response_model=NodesOut)
    async def get_nodes(
            self,
            label: str,
            response: Response,
            properties_keys: Union[List[str], None] = Query(default=None),
            properties_values: Union[List[str], None] = Query(default=None),
    ):
        """
        Get nodes with same label as given
        """
        nodes = self.node_service.get_nodes(
            label, properties_keys=properties_keys, properties_values=properties_values
        )
        if nodes.errors is not None:
            response.status_code = 422

        nodes.links = get_links(router)

        return nodes

    @router.delete("/nodes/{id}", tags=["nodes"], response_model=NodeOut)
    async def delete_node(self, id: int, response: Response):
        """
        Delete node by id
        """
        delete_response = self.node_service.delete_node(id)
        if delete_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        delete_response.links = get_links(router)

        return delete_response

    @router.get("/nodes/{id}/relationships", tags=["nodes"], response_model=RelationshipsOut)
    async def get_node_relationships(self, id: int, response: Response):
        """
        Get relationships for node with given id
        """
        get_response = self.node_service.get_relationships(id)
        if get_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        get_response.links = get_links(router)

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

    @router.delete("/nodes/{id}/properties", tags=["nodes"], response_model=NodeOut)
    async def delete_node_properties(self, id: int, response: Response):
        """
        Delete node properties by id
        """
        delete_response = self.node_service.delete_node_properties(id)
        if delete_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        delete_response.links = get_links(router)

        return delete_response
