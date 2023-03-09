import asyncio
import unittest
import unittest.mock as mock

from recording.recording_router import *
from recording.recording_service_graphdb import RecordingServiceGraphDB


class TestRecordingRouterPost(unittest.TestCase):

    @mock.patch.object(RecordingServiceGraphDB, 'save_recording')
    def test_create_recording_without_error(self, save_recording_mock):
        database_name = "neo4j"
        save_recording_mock.return_value = RecordingOut(participation_id=3, registered_channel_id=2, id=1)
        response = Response()
        recording = RecordingIn(participation_id=3, registered_channel_id=2)
        recording_router = RecordingRouter()

        result = asyncio.run(recording_router.create_recording(recording, response, database_name))

        self.assertEqual(result, RecordingOut(participation_id=3, registered_channel_id=2, id=1,
                                              links=get_links(router)))
        save_recording_mock.assert_called_once_with(recording, database_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RecordingServiceGraphDB, 'save_recording')
    def test_create_recording_with_error(self, save_recording_mock):
        database_name = "neo4j"
        save_recording_mock.return_value = RecordingOut(participation_id=3, registered_channel_id=2, id=1,
                                                        errors={'errors': ['test']})
        response = Response()
        recording = RecordingIn(participation_id=3, registered_channel_id=2)
        recording_router = RecordingRouter()

        result = asyncio.run(recording_router.create_recording(recording, response, database_name))

        self.assertEqual(result, RecordingOut(participation_id=3, registered_channel_id=2, id=1,
                                              errors={'errors': ['test']}, links=get_links(router)))
        save_recording_mock.assert_called_once_with(recording, database_name)
        self.assertEqual(response.status_code, 422)
