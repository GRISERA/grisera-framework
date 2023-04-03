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

    def create_dataset(self, database_name_to_create: str):
        """
        Send request to database by its API to create new dataset

        Returns:
            Result of request as dataset object
        """

        response = self.db.create_database_with_name(database_name_to_create)

        if len(response["errors"]) > 0:
            result = DatasetOut(errors=response["errors"])
        else:
            result = DatasetOut(name=str(database_name_to_create))

        return result

    def get_dataset_by_name(self, database_name_looked_for: str):
        """
        Send request to database by its API to acquire all nodes with given label

        Args:
            database_name (string): Name of the database

        Returns:
            List of acquired nodes in NodesOut model
        """
        found = self.db.check_if_database_exists(database_name_looked_for)

        if not found:
            return DatasetOut(errors="Dataset not found")

        return DatasetOut(name=database_name_looked_for)

    def get_datasets(self, database_name: str):
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

        for dataset in response["results"][0]["data"]:
            result.datasets.append(BasicDatasetOut(name=dataset['row'][0]))

        return result

    def delete_dataset(self, database_name_looked_for: str):
        """
        Send request to database by its API to delete node with given id

        Args:
            node_id (int): Id of node
            database_name (string): Name of the database
        Returns:
            Deleted node
        """
        dataset = self.get_dataset_by_name(database_name_looked_for)
        response = self.db.delete_dataset(database_name_looked_for)
        result = DatasetOut(errors=response["errors"]) if len(response["errors"]) > 0 else \
            DatasetOut(name=database_name_looked_for)

        return result
