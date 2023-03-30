from dataset.dataset_service import DatasetService
from graph_api_service import GraphApiService
from dataset.dataset_model import DatasetOut, DatasetIn, DatasetsOut, BasicDatasetOut
from models.not_found_model import NotFoundByIdModel
from models.relation_information_model import RelationInformation


class DatasetServiceGraphDB(DatasetService):
    """
    Object to handle logic of datasets requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_dataset(self, database_name_to_create: str):
        """
        Send request to database by its API to create new relationship

        Args:
            relationship (-): Relationship to be added to database

        Returns:
            Result of request as relationship object
        """

        response = self.graph_api_service.create_database(database_name_to_create)

        if response["errors"] is not None:
            return DatasetsOut(name=database_name_to_create, errors=response["errors"])

        return DatasetOut(name=database_name_to_create)

    def get_dataset(self, database_name):
        """
        Send request to database by its API to acquire all nodes with given label

        Args:
            database_name (string): Name of the database

        Returns:
            List of acquired nodes in NodesOut model
        """
        get_response = self.graph_api_service.get_node("Dataset", database_name)

        if get_response["errors"] is not None:
            return DatasetOut(errors=get_response["errors"])

        result = DatasetOut()

        # TODO: cos jest zle autentycznie
        return result  # tu moze trzeba bedzie zrobic result.datasets

    def get_datasets(self, database_name):
        """
        Send request to database by its API to acquire all nodes with given label

        Args:
            database_name (string): Name of the database

        Returns:
            List of acquired nodes in NodesOut model
        """
        get_response = self.graph_api_service.get_databases()

        if get_response["errors"] is not None:
            return DatasetsOut(errors=get_response["errors"])

        result = DatasetsOut(datasets=[])

        for dataset in get_response["datasets"]:
            result.datasets.append(BasicDatasetOut(name=dataset['name']))

        return DatasetsOut(datasets=result.datasets)

    def delete_dataset(self, database_name: str):
        """
        Send request to graph api to delete given dataset

        Args:
        database_name (str): Name of a dataset

        Returns:
            Result of request as dataset object
        """
        get_response = self.get_dataset(database_name)

        if type(get_response) is NotFoundByIdModel:
            return get_response

        self.graph_api_service.delete_node(database_name)
        return get_response
