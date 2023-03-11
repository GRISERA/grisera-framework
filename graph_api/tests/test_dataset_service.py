import unittest
import unittest.mock as mock

from database_service import DatabaseService
from dataset.dataset_model import *
from dataset.dataset_service import DatasetService


class TestDatasetService(unittest.TestCase):

    def setUp(self):
        self.database_name = "neo4j"

    @mock.patch.object(DatabaseService, 'create_database_with_name')
    def test_create_dataset_without_error(self, create_database_with_name_mock):
        create_database_with_name_mock.return_value = {'results': [{'data': []}], 'errors': []}

        database_name_to_create = "test"
        dataset_service = DatasetService()

        result = dataset_service.create_dataset(database_name_to_create)

        self.assertEqual(result, DatasetOut(name="test", errors=None))
        create_database_with_name_mock.assert_called_once_with(database_name_to_create)

    @mock.patch.object(DatabaseService, 'create_database_with_name')
    def test_create_dataset_with_error(self, create_database_with_name_mock):
        create_database_with_name_mock.return_value = {'results': [{'data': []}], 'errors': []}
        database_name_to_create = "test"
        dataset_service = DatasetService()
        database_name = "neo4j"

        result = dataset_service.create_dataset(database_name_to_create)

        self.assertEqual(result, DatasetOut(name="test", errors=None))
        create_database_with_name_mock.assert_called_once_with(database_name_to_create)

    @mock.patch.object(DatabaseService, 'show_databases_with_name')
    def test_get_datasets_without_error(self, get_datasets_mock):
        get_datasets_mock.return_value = {'results': [{'data': [{'row': ['neo4j']}]}], 'errors': []}

        dataset_service = DatasetService()

        result = dataset_service.get_datasets(self.database_name)

        self.assertEqual(result, DatasetsOut(errors=None, datasets=[BasicDatasetOut(name="neo4j")]))
        get_datasets_mock.assert_called_once_with(self.database_name)

    @mock.patch.object(DatabaseService, 'show_databases_with_name')
    def test_get_datasets_with_error(self, get_datasets_mock):
        get_datasets_mock.return_value = {'results': [{'data': [{'meta': [{}]}]}], 'errors': ['error']}
        dataset_service = DatasetService()

        result = dataset_service.get_datasets(self.database_name)

        self.assertEqual(result, DatasetsOut(errors=['error']))
        get_datasets_mock.assert_called_once_with(self.database_name)
