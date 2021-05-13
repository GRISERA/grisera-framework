import json
import unittest
import unittest.mock as mock
from recording.recording_model import *
from recording.recording_service import RecordingService
from requests import Response


class TestRecordingPostService(unittest.TestCase):

    @mock.patch('graph_api_service.requests')
    def test_recordings_service_without_error(self, mock_requests):
        response = Response()
        response._content = json.dumps({'id': 1, 'properties': None, "errors": None,
                                        'links': None}).encode('utf-8')
        mock_requests.post.return_value = response
        recordings = RecordingsIn(activities=[1], participant_state_id=1)
        recording_service = RecordingService()

        result = recording_service.save_recordings(recordings)

        self.assertEqual(result, RecordingsOut(recordings=[RecordingOut(activity_id=1, participant_state_id=1, id=1)]))
