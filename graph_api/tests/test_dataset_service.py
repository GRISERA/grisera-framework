import unittest
import unittest.mock as mock

from database_service import DatabaseService
from dataset.dataset_model import *
from dataset.dataset_service import DatasetService


class TestDatasetService(unittest.TestCase):

    def setUp(self):
        self.database_name = "neo4j"

    @mock.patch.object(DatabaseService, 'create_dataset')
    def test_create_dataset_without_error(self, create_database_with_name_mock):
        create_database_with_name_mock.return_value = {'results': [{'data': []}], 'errors': []}

        database_name_to_create = "test"
        dataset_service = DatasetService()

        result = dataset_service.create_dataset(database_name_to_create)

        self.assertEqual(result, DatasetOut(name_hash=result.name_hash, name_by_user="test", errors=None))
        create_database_with_name_mock.assert_called_once_with(result.name_hash)

    @mock.patch.object(DatabaseService, 'create_dataset')
    def test_create_dataset_with_error(self, create_database_with_name_mock):
        create_database_with_name_mock.return_value = {'results': [{'data': []}], 'errors': ['error']}
        database_name_to_create = "test"
        dataset_service = DatasetService()

        result = dataset_service.create_dataset(database_name_to_create)
        self.assertEqual(result, DatasetOut(name_hash=None, name_by_user =None , errors=['error']))

    @mock.patch.object(DatabaseService, 'get_datasets')
    def test_get_datasets_without_error(self, get_datasets_mock):
        get_datasets_mock.return_value = {'results': [{'data': [{'row': ['neo4j']}]}], 'errors': []}

        dataset_service = DatasetService()

        result = dataset_service.get_datasets()

        self.assertEqual(result, DatasetsOut(errors=None, datasets=[BasicDatasetOut(name_hash="neo4j")]))
        get_datasets_mock.assert_called_once_with("neo4j")

    @mock.patch.object(DatabaseService, 'get_datasets')
    def test_get_datasets_with_error(self, get_datasets_mock):
        get_datasets_mock.return_value = {'results': [{'data': [{'meta': [{}]}]}], 'errors': ['error']}
        dataset_service = DatasetService()

        result = dataset_service.get_datasets()

        self.assertEqual(result, DatasetsOut(errors=['error']))
        get_datasets_mock.assert_called_once_with(self.database_name)

    @mock.patch.object(DatabaseService, 'dataset_exists')
    def test_get_dataset_without_error(self, get_dataset_mock):
        get_dataset_mock.return_value = {'results': [{'data': []}], 'errors': []}

        dataset_service = DatasetService()

        result = dataset_service.get_dataset(name_hash="neo4j")

        self.assertEqual(result, DatasetOut(name_hash=result.name_hash, name_by_user="test", errors=None))
        get_dataset_mock.assert_called_once_with("neo4j")

    @mock.patch.object(DatabaseService, 'delete_dataset')
    def test_delete_dataset_without_error(self, delete_dataset_mock):
        delete_dataset_mock.return_value = {'results': [{'data': []}], 'errors': []}
        dataset_service = DatasetService()
        result = dataset_service.delete_dataset("test")

        self.assertEqual(result, DatasetOut(name_hash=result.name_hash, name_by_user=result.name_by_user,errors=None))
        delete_dataset_mock.assert_called_once_with("test")


    @mock.patch.object(DatabaseService, 'delete_dataset')
    def test_delete_dataset_with_error(self, delete_dataset_mock):
        delete_dataset_mock.return_value = {'results': [{'data': []}], 'errors': ['error']}
        dataset_service = DatasetService()
        result = dataset_service.delete_dataset("test")

        self.assertEqual(result, DatasetOut(name_hash=result.name_hash, name_by_user=result.name_by_user,errors=['error']))
        delete_dataset_mock.assert_called_once_with("test")

