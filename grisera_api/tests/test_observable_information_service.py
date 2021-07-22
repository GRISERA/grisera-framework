import json
import unittest
import unittest.mock as mock
from observable_information.observable_information_model import *
from observable_information.observable_information_service import ObservableInformationService
from requests import Response


class TestObservableInformationPostService(unittest.TestCase):

    @mock.patch('graph_api_service.requests')
    def test_observable_information_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': 1, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        observable_information = ObservableInformationIn(modality="body posture", live_activity="muscles activity")
        observable_information_service = ObservableInformationService()

        result = observable_information_service.save_observable_information(observable_information)

        self.assertEqual(result, ObservableInformationOut(modality="body posture", live_activity="muscles activity",
                                                          id=1))

    @mock.patch('graph_api_service.requests')
    def test_observable_information_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': None, 'properties': None, "errors": {'error': 'test'},
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        observable_information = ObservableInformationIn(modality="body posture", live_activity="muscles activity")
        observable_information_service = ObservableInformationService()

        result = observable_information_service.save_observable_information(observable_information)

        self.assertEqual(result, ObservableInformationOut(modality="body posture", live_activity="muscles activity",
                                                          errors={'error': 'test'}))
