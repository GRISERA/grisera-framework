from dataset.dataset_service import DatasetService
from graph_api_service import GraphApiService
from dataset.dataset_model import DatasetOut, DatasetIn, DatasetsOut, BasicDatasetOut
from models.not_found_model import NotFoundByIdModel


class DatasetServiceGraphDB(DatasetService):
    """
    Object to handle logic of datasets requests

    Attributes:
    graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_dataset(self, dataset_name: str):
        """
        Send request to database by its API to create new dataset

        Args:
            dataset_name (str): Name of the dataset to be created

        Returns:
            Result of request as dataset object
        """
        dataset_name = dataset_name.lower()  # convert the dataset name to lowercase

        response = self.graph_api_service.create_dataset(dataset_name)

        if response["errors"] is not None:
            return DatasetsOut(name_hash=dataset_name, errors=response["errors"])

        return DatasetOut(name_hash=response["name_hash"], name_by_user=response["name_by_user"])

    def get_dataset(self, dataset_name):
        """
        Send request to database by its API to acquire dataset with particular name

        Args:
            dataset_name (string): Name of the searched dataset

        Returns:
            Acquired dataset in DatasetOut model
        """
        get_response = self.graph_api_service.get_dataset(dataset_name)

        if get_response["errors"] is not None:
            return DatasetOut(errors=get_response["errors"])

        result = DatasetOut(name_hash=get_response["name_hash"], name_by_user=get_response["name_by_user"])

        return result

    def get_datasets(self):
        """
        Send request to database by its API to acquire all nodes with given label

        Returns:
            List of acquired nodes in NodesOut model
        """
        get_response = self.graph_api_service.get_datasets()

        if get_response["errors"] is not None:
            return DatasetsOut(errors=get_response["errors"])

        result = DatasetsOut(datasets=[])

        for dataset in get_response["datasets"]:
            result.datasets.append(BasicDatasetOut(name_hash=dataset['name_hash']))

        return DatasetsOut(datasets=result.datasets)

    def delete_dataset(self, database_name_looked_for: str):
        """
        Send request to graph api to delete given dataset

        Args:
        database_name (str): Name of a dataset

        Returns:
            Result of request as dataset object
        """
        delete_response = self.get_dataset(database_name_looked_for)

        if type(delete_response) is NotFoundByIdModel:
            return delete_response

        self.graph_api_service.delete_dataset(database_name_looked_for)
        return delete_response
