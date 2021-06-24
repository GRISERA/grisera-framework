import json
import unittest
import unittest.mock as mock
from activity.activity_model import *
from recording.recording_model import *
from recording.recording_service import RecordingService
from requests import Response


class TestRecordingPostService(unittest.TestCase):

    @mock.patch('graph_api_service.requests')
    def test_recording_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': 1, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        recording = RecordingIn(participation_id=3, registered_channel_id=2)
        recording_service = RecordingService()

        result = recording_service.save_recording(recording)

        self.assertEqual(result, RecordingOut(participation_id=3, registered_channel_id=2, id=1))

    @mock.patch('graph_api_service.requests')
    def test_recording_service_with_error(self, mock_requests):
        response = Response()
        response._content = json.dumps(
            {'id': None, 'properties': None, "errors": {'error': 'test'}, 'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        recording = RecordingIn(participation_id=3, registered_channel_id=2)
        recording_service = RecordingService()

        result = recording_service.save_recording(recording)

        self.assertEqual(result, RecordingOut(participation_id=3, registered_channel_id=2, errors={'error': 'test'}))
