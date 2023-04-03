from typing import Optional, Any, List
from pydantic import BaseModel
from property.property_model import PropertyIn


class DatasetIn(BaseModel):
    """
        Model of relationship to acquire from client

        Attributes:
            start_node (Optional[int]): Id of node which starts connection
            end_node (Optional[int]): Id of node which ends connection
            name (Optional[str]): Name of the relationship
    """

    name: str = None


class BasicDatasetOut(DatasetIn):
    """
        Model of relationship in database

        Attributes:
            id (Optional[int]): Id of relationship returned from graph database
            propeties(Optional[List[PropertyIn]]): List of properties of the relationship in the database

    """
    name: str = None


class DatasetOut(DatasetIn):
    """
        Model of relationship to send to client as a result of request

        Attributes:
            errors (Optional[Any]): Optional errors appeared during query executions
            links (Optional[list): Hateoas implementation
    """
    errors: Optional[Any] = None
    links: Optional[list] = None


class DatasetsOut(BaseModel):
    """
    Model of list of nodes

    Attributes:
        nodes (Optional[List[BasicNodeOut]]): List of nodes to send
        errors (Optional[Any]): Optional errors appeared during query executions
        links (Optional[list): Hateoas implementation
    """
    datasets: Optional[List[BasicDatasetOut]] = None
    errors: Optional[Any] = None
    links: Optional[List] = None
