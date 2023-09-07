from dataset.dataset_service import DatasetService
from dataset.dataset_model import DatasetOut, DatasetIn, DatasetsOut, BasicDatasetOut
from ontology_api_service import OntologyApiService


class DatasetServiceOntology(DatasetService):
    """
    Object to handle logic of datasets requests

    Attributes:
    ontology_api_service (ExperimentService): Service used to communicate with Ontology API
    """
    ontology_api_service = OntologyApiService()

    def save_dataset(self, dataset_name_to_create: str):
        """
        Send request to ontology api to add new dataset

        Args:
            dataset_name_to_create (str): dataset name to be created

        Returns:
            Result of request as dataset object
        """
        raise Exception("Reference to an unimplemented method.")

    def get_dataset(self, dataset_name):
        raise Exception("Reference to an unimplemented method.")

    def get_datasets(self, dataset_name):
        raise Exception("Reference to an unimplemented method.")

    def delete_dataset(self, dataset_name: str):
        raise Exception("Reference to an unimplemented method.")
