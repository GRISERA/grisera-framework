import unittest
import unittest.mock as mock

from measure_name.measure_name_model import *
from measure_name.measure_name_service import MeasureNameService
from graph_api_service import GraphApiService


class TestMeasureNameService(unittest.TestCase):

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_measure_name_without_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'properties': [{'key': 'name', 'value': 'Liking'},
                                                                             {'key': 'type', 'value': 'Ekman model measure'}],
                                               "errors": None, 'links': None}
        measure_name = MeasureNameIn(name='Liking', type='Ekman model measure')
        measure_name_service = MeasureNameService()

        result = measure_name_service.save_measure_name(measure_name)

        self.assertEqual(result, MeasureNameOut(id=id_node, name='Liking', type='Ekman model measure'))
        create_node_mock.assert_called_once_with('`Measure Name`')
        create_properties_mock.assert_called_once_with(id_node, measure_name)

    @mock.patch.object(GraphApiService, 'create_node')
    def test_save_measure_name_with_node_error(self, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": ['error'], 'links': None}
        measure_name = MeasureNameIn(name='Liking', type='Ekman model measure')
        measure_name_service = MeasureNameService()

        result = measure_name_service.save_measure_name(measure_name)

        self.assertEqual(result, MeasureNameOut(name='Liking', type='Ekman model measure', errors=['error']))
        create_node_mock.assert_called_once_with('`Measure Name`')

    @mock.patch.object(GraphApiService, 'create_node')
    @mock.patch.object(GraphApiService, 'create_properties')
    def test_save_measure_name_with_properties_error(self, create_properties_mock, create_node_mock):
        id_node = 1
        create_node_mock.return_value = {'id': id_node, 'properties': None, "errors": None, 'links': None}
        create_properties_mock.return_value = {'id': id_node, 'errors': ['error'], 'links': None}
        measure_name = MeasureNameIn(name='Liking', type='Ekman model measure')
        measure_name_service = MeasureNameService()

        result = measure_name_service.save_measure_name(measure_name)

        self.assertEqual(result, MeasureNameOut(name='Liking', type='Ekman model measure', errors=['error']))
        create_node_mock.assert_called_once_with('`Measure Name`')
        create_properties_mock.assert_called_once_with(id_node, measure_name)

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_measure_names_without_error(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': [{'id': 1,
                                                  'properties': [{'key': 'name', 'value': 'Liking'},
                                                                 {'key': 'type', 'value': 'Ekman model measure'}]},
                                                 {'id': 2,
                                                  'properties': [{'key': 'name', 'value': 'Liking'},
                                                                 {'key': 'type', 'value': 'Ekman model measure'}]}
                                                 ],
                                       "errors": None, 'links': None}
        measure_name_service = MeasureNameService()

        result = measure_name_service.get_measure_names()

        get_nodes_mock.assert_called_once_with('`Measure Name`')
        self.assertEqual(result, MeasureNamesOut(measure_names=[BasicMeasureNameOut(id=1, name='Liking',
                                                                               type='Ekman model measure'),
                                                           BasicMeasureNameOut(id=2, name='Liking',
                                                                               type='Ekman model measure')]))

    @mock.patch.object(GraphApiService, 'get_nodes')
    def test_get_measure_names_with_error(self, get_nodes_mock):
        get_nodes_mock.return_value = {'nodes': None, "errors": ['error'], 'links': None}
        measure_name_service = MeasureNameService()

        result = measure_name_service.get_measure_names()

        get_nodes_mock.assert_called_once_with('`Measure Name`')
        self.assertEqual(result, MeasureNamesOut(errors=['error']))
