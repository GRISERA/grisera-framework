from typing import List

from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from hateoas import get_links
from node.node_model import NodeIn, NodeOut, NodesOut, NodeRowsOut, NodeRowsQueryIn
from node.node_service import NodeService
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
    async def create_node(self, node: NodeIn, database_name: str, response: Response):
        """
        Create node with optional labels
        """
        create_response = self.node_service.save_node(node, database_name)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/nodes/{id}", tags=["nodes"], response_model=NodeOut)
    async def get_node(self, id: int, response: Response, database_name: str):
        """
        Get node with same id as given
        """
        node = self.node_service.get_node(id, database_name)
        if node.errors is not None:
            response.status_code = 404

        node.links = get_links(router)

        return node

    @router.get("/nodes", tags=["nodes"], response_model=NodesOut)
    async def get_nodes(self, label: str, response: Response, database_name: str):
        """
        Get nodes with same label as given
        """
        nodes = self.node_service.get_nodes(label, database_name)
        if nodes.errors is not None:
            response.status_code = 422

        nodes.links = get_links(router)

        return nodes

    @router.post("/nodes_query", tags=["nodes"], response_model=NodeRowsOut)
    async def get_nodes_by_query(self, query: NodeRowsQueryIn, response: Response, database_name: str):
        """
        Get nodes with same query as given
        """
        nodes = self.node_service.get_nodes_by_query(query, database_name)
        if nodes.errors is not None:
            response.status_code = 422

        nodes.links = get_links(router)

        return nodes

    @router.delete("/nodes/{id}", tags=["nodes"], response_model=NodeOut)
    async def delete_node(self, id: int, response: Response, database_name: str):
        """
        Delete node by id
        """
        delete_response = self.node_service.delete_node(id,database_name)
        if delete_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        delete_response.links = get_links(router)

        return delete_response

    @router.get("/nodes/{id}/relationships", tags=["nodes"], response_model=RelationshipsOut)
    async def get_node_relationships(self, id: int, response: Response, database_name: str):
        """
        Get relationships for node with given id
        """
        get_response = self.node_service.get_relationships(id,database_name)
        if get_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.post("/nodes/{id}/properties", tags=["nodes"], response_model=NodeOut)
    async def create_node_properties(self, id: int, properties: List[PropertyIn], response: Response, database_name: str):
        """
        Create properties for node with given id
        """
        create_response = self.node_service.save_properties(id, properties, database_name)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.delete("/nodes/{id}/properties", tags=["nodes"], response_model=NodeOut)
    async def delete_node_properties(self, id: int, response: Response, database_name: str):
        """
        Delete node properties by id
        """
        delete_response = self.node_service.delete_node_properties(id,database_name)
        if delete_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        delete_response.links = get_links(router)

        return delete_response
