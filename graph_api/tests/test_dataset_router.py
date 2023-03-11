import asyncio
import unittest
import unittest.mock as mock

from dataset.dataset_router import *
from dataset.dataset_model import *


def return_dataset(*args, **kwargs):
    return DatasetOut(name="test", errors=None)


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
        database_name_to_create = "test"
        result = asyncio.run(dataset_router.create_dataset(response, database_name_to_create))

        self.assertEqual(result, DatasetOut(name="test", errors=None))
        create_dataset_mock.assert_called_with(database_name_to_create)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(DatasetService, 'create_dataset')
    def test_create_dataset_with_error(self, create_dataset_mock):
        create_dataset_mock.return_value = DatasetOut(name="test", errors={'errors': ['test']},links=get_links(router))
        response = Response()
        dataset_router = DatasetRouter()
        database_name_to_create = "test"

        result = asyncio.run(dataset_router.create_dataset(response, database_name_to_create))

        self.assertEqual(result, DatasetOut(name='test', errors={'errors': ['test']}))
        create_dataset_mock.assert_called_with(dataset, self.database_name)
        self.assertEqual(response.status_code, 422)

    @mock.patch.object(DatasetService, 'get_datasets')
    def test_get_datasets_without_error(self, get_datasets_mock):
        get_datasets_mock.side_effect = return_datasets
        response = Response()

        dataset_router = DatasetRouter()

        result = asyncio.run(dataset_router.get_datasets(response))

        self.assertEqual(result, DatasetsOut(errors=None, datasets=[BasicDatasetOut(name="test")], links=get_links(router)))

        self.assertEqual(response.status_code, 200)

    @mock.patch.object(DatasetService, 'get_datasets')
    def test_get_datasets_with_error(self, get_datasets_mock):
        get_datasets_mock.return_value = DatasetsOut(errors={'errors': ['test']})
        response = Response()
        dataset_router = DatasetRouter()

        result = asyncio.run(dataset_router.get_datasets(response))

        self.assertEqual(result, DatasetsOut(errors={'errors': ['test']}, links=get_links(router)))

        self.assertEqual(response.status_code, 4)
