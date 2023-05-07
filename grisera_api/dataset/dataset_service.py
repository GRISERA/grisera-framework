from graph_api_service import GraphApiService
from dataset.dataset_model import DatasetOut, DatasetIn, DatasetsOut, BasicDatasetOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class DatasetService:
    """
    Object to handle logic of relationships requests

    Attributes:
        db (DatabaseService): Handles communication with Neo4j database
    """
    graph_api_service = GraphApiService()

    def save_dataset(self, dataset_name_to_create: str):
        """
        Send request to database by its API to create new relationship

        Args:
            relationship (-): Relationship to be added to database

        Returns:
            Result of request as relationship object
        """

        raise Exception("save_database not implemented yet")

    def get_datasets(self, dataset_name):
        """
        Send request to database by its API to acquire all nodes with given label

        Args:
            database_name (string): Name of the database

        Returns:
            List of acquired nodes in NodesOut model
        """
        raise Exception("get_datasets not implemented yet")
    
    def get_dataset(self, dataset_name: str):
        """
        Send request to graph api to get given experiment

        Args:
        database_name (str): name of dataset

        Returns:
            Result of request as experiment object
        """
        raise Exception("get_dataset not implemented yet")
    
    def delete_dataset(self, dataset_name: str):
        """
        Send request to graph api to delete given experiment

        Args:
        database_name (str): name of dataset

        Returns:
            Result of request as experiment object
        """
        raise Exception("delete_dataset not implemented yet")
