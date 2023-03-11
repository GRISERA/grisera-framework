import asyncio
import unittest
import unittest.mock as mock

from dataset.dataset_router import *


def return_dataset(*args, **kwargs):
    return DatasetOut(name="test", errors=None)


def return_dataset_delete(*args, **kwargs):
    return DatasetOut(name="test", errors=None)


class TestDatasetRouter(unittest.TestCase):

    def setUp(self):
        self.database_name = "neo4j"

    @mock.patch.object(DatasetService, 'save_dataset')
    def test_create_dataset_without_error(self, save_dataset_mock):
        save_dataset_mock.side_effect = return_dataset
        response = Response()
        dataset = DatasetIn(name="test")
        dataset_router = DatasetRouter()

        result = asyncio.run(dataset_router.create_dataset(dataset, response, self.database_name))

        self.assertEqual(result, DatasetOut(name="test", errors=None))
        save_dataset_mock.assert_called_with(dataset, self.database_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(DatasetService, 'save_dataset')
    def test_create_dataset_with_error(self, save_dataset_mock):
        save_dataset_mock.return_value = DatasetOut(name="test", errors={'errors': ['test']})
        response = Response()
        dataset = DatasetIn(name="test")
        dataset_router = DatasetRouter()

        result = asyncio.run(dataset_router.create_dataset(dataset, response, self.database_name))

        self.assertEqual(result, DatasetOut(errors={'errors': ['test']})) # tu moze byc error
        save_dataset_mock.assert_called_with(dataset, self.database_name)
        self.assertEqual(response.status_code, 422)

    @mock.patch.object(DatasetService, 'get_dataset')
    def test_get_dataset_without_error(self, get_dataset_mock):
        get_dataset_mock.side_effect = return_dataset
        response = Response()
        
        dataset_router = DatasetRouter()

        result = asyncio.run(dataset_router.get_node(5, response, self.database_name))

        self.assertEqual(result, DatasetOut(name="test", errors=None))
        get_dataset_mock.assert_called_with(5, self.database_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(DatasetService, 'get_dataset')
    def test_get_dataset_with_error(self, get_dataset_mock):
        get_dataset_mock.return_value = DatasetOut(name="test", errors='test')
        response = Response()
        label = "Test"
        dataset_router = DatasetRouter()

        result = asyncio.run(dataset_router.get_dataset(response, self.database_name))

        self.assertEqual(result, DatasetOut(name="test", errors='test'))
        get_dataset_mock.assert_not_called()
        self.assertEqual(response.status_code, 404)
