import asyncio
import unittest
import unittest.mock as mock

from grisera_api.recording.recording_router import *
from grisera_api.recording.recording_service_graphdb import RecordingServiceGraphDB


class TestRecordingRouterDelete(unittest.TestCase):

    @mock.patch.object(RecordingServiceGraphDB, 'delete_recording')
    def test_delete_recording_without_error(self, delete_recording_mock):
        recording_id = 1
        delete_recording_mock.return_value = RecordingOut(id=recording_id)
        response = Response()
        recording_router = RecordingRouter()

        result = asyncio.run(recording_router.delete_recording(recording_id, response))

        self.assertEqual(result, RecordingOut(id=recording_id, links=get_links(router)))
        delete_recording_mock.assert_called_once_with(recording_id)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RecordingServiceGraphDB, 'delete_recording')
    def test_delete_recording_with_error(self, delete_recording_mock):
        delete_recording_mock.return_value = RecordingOut(errors={'errors': ['test']})
        response = Response()
        recording_id = 1
        recording_router = RecordingRouter()

        result = asyncio.run(recording_router.delete_recording(recording_id, response))

        self.assertEqual(result, RecordingOut(errors={'errors': ['test']}, links=get_links(router)))
        delete_recording_mock.assert_called_once_with(recording_id)
        self.assertEqual(response.status_code, 404)
