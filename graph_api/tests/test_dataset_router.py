import asyncio
import unittest
import unittest.mock as mock

from dataset.dataset_router import *
from dataset.dataset_model import *


def return_dataset(*args, **kwargs):
    return DatasetOut(name_hash="neo4j", name_by_user="test", errors=None)

def return_dataset_delete(*args, **kwargs):
    return DatasetOut(name="test", errors=None)


def return_datasets(*args, **kwargs):
    return DatasetsOut(datasets=[BasicDatasetOut(name="test")])


class TestDatasetRouter(unittest.TestCase):

    def setUp(self):
        self.database_name = "neo4j"

    @mock.patch.object(DatasetService, 'create_dataset')
    def test_create_dataset_without_error(self, create_dataset_mock):
        create_dataset_mock.side_effect = return_dataset
        response = Response()
        dataset_router = DatasetRouter()
        dataset = DatasetIn(name_hash="neo4j", name_by_user="test")
        result = asyncio.run(dataset_router.create_dataset(dataset, response))
        result.name_hash = "neo4j"
        self.assertEqual(result,
                         DatasetOut(name_hash="neo4j", name_by_user="test", errors=None, links=get_links(router)))
        create_dataset_mock.assert_called_with('test')
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(DatasetService, 'create_dataset')
    def test_create_dataset_with_error(self, create_dataset_mock):
        create_dataset_mock.return_value = DatasetOut(name_by_user="test", errors={'errors': ['test']})
        response = Response()
        dataset_router = DatasetRouter()
        dataset = DatasetIn(name_hash="neo4j", name_by_user="test")
        result = asyncio.run(dataset_router.create_dataset(dataset, response))
        self.assertEqual(result, DatasetOut(name_by_user='test', errors={'errors': ['test']}, links=get_links(router)))
        create_dataset_mock.assert_called_with("test")
        self.assertEqual(response.status_code, 422)

    @mock.patch.object(DatasetService, 'get_dataset')
    def test_get_dataset_without_error(self, get_dataset_mock):
        get_dataset_mock.side_effect = return_dataset
        response = Response()
        dataset_router = DatasetRouter()

        result = asyncio.run(dataset_router.get_dataset("neo4j", response))
        self.assertEqual(result,
                         DatasetOut(name_hash="neo4j", name_by_user="test", errors=None, links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(DatasetService, 'get_dataset')
    def test_get_dataset_with_error(self, get_dataset_mock):
        get_dataset_mock.return_value = DatasetOut(name_by_user="test", errors={'errors': ['test']})
        response = Response()
        dataset_router = DatasetRouter()

        result = asyncio.run(dataset_router.get_dataset("neo4j", response))

        self.assertEqual(result, DatasetOut(name_by_user="test", errors={'errors': ['test']}, links=get_links(router)))

        self.assertEqual(response.status_code, 422)

    @mock.patch.object(DatasetService, 'get_datasets')
    def test_get_datasets_without_error(self, get_datasets_mock):
        get_datasets_mock.side_effect = return_datasets
        response = Response()

        dataset_router = DatasetRouter()

        result = asyncio.run(dataset_router.get_datasets(response))

        self.assertEqual(result, DatasetsOut(errors=None, datasets=[BasicDatasetOut(name_by_user="test")], links=get_links(router)))

        self.assertEqual(response.status_code, 200)

    @mock.patch.object(DatasetService, 'get_datasets')
    def test_get_datasets_with_error(self, get_datasets_mock):
        get_datasets_mock.return_value = DatasetsOut(errors={'errors': ['test']})
        response = Response()
        dataset_router = DatasetRouter()

        result = asyncio.run(dataset_router.get_datasets(response))

        self.assertEqual(result, DatasetsOut(errors={'errors': ['test']}, links=get_links(router)))

        self.assertEqual(response.status_code, 422)


    @mock.patch.object(DatasetService, 'delete_dataset')
    def test_delete_dataset_without_error(self, delete_dataset_mock):
        delete_dataset_mock.side_effect = return_dataset
        response = Response()
        dataset_router = DatasetRouter()
        result = asyncio.run(dataset_router.delete_dataset(response, dataset_name="test"))

        self.assertEqual(result,
                         DatasetOut(name_hash="neo4j", name_by_user="test", errors=None, links=get_links(router)))
        self.assertEqual(response.status_code, 200)


    @mock.patch.object(DatasetService, 'delete_dataset')
    def test_delete_dataset_with_error(self, delete_dataset_mock):
        delete_dataset_mock.return_value = DatasetOut(name_hash="neo4j",name_by_user="test", errors={'errors': ['neo4j']})
        response = Response()
        dataset_router = DatasetRouter()
        result = asyncio.run(dataset_router.delete_dataset(response, dataset_name="test"))
        self.assertEqual(result, DatasetOut(name_hash="neo4j", name_by_user="test", errors={'errors': ['neo4j']}, links=get_links(router)))

        self.assertEqual(response.status_code, 404)
