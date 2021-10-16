from pydantic import BaseModel


class RelationInformation(BaseModel):
    """
    Simplified model of relation, which passes information

    Attributes:
        second_node_id (int): Id of second node of relation. It can be start node or end node.
        name (str): Name of relationship.
    """
    second_node_id: int
    name: str
