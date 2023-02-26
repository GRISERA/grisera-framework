from database_service import DatabaseService
from database_config import database
from dataset.dataset_model import DatasetOut, DatasetIn, DatasetsOut, BasicDatasetOut
from property.property_model import PropertyIn
from typing import List


class DatasetService:
    """
    Object to handle logic of relationships requests

    Attributes:
        db (DatabaseService): Handles communication with Neo4j database
    """
    db: DatabaseService = DatabaseService()

    def create_dataset(self, dataset: DatasetIn, database_name_to_create: str, database_name: str):
        """
        Send request to database by its API to create new relationship

        Args:
            relationship (-): Relationship to be added to database

        Returns:
            Result of request as relationship object
        """

        response = self.db.create_database_with_name(database_name_to_create, database_name)
        if len(response["errors"]) > 0:
            result = DatasetOut(errors=response["errors"])
        else:
            result = DatasetOut(name=database_name)

        return result

    def get_datasets(self, database_name):
        """
        Send request to database by its API to acquire all nodes with given label

        Args:
            database_name (string): Name of the database

        Returns:
            List of acquired nodes in NodesOut model
        """
        response = self.db.show_databases_with_name(database_name)
        if len(response["errors"]) > 0:
            return DatasetsOut(errors=response["errors"])
        
        result = DatasetsOut(datasets=[])
        for node in response["results"][0]["data"]:
            name = node['row'][0]
            result.datasets.append(BasicDatasetOut(name=name))

        return result
