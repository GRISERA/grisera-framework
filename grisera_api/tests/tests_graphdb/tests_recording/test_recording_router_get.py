import asyncio
import unittest
import unittest.mock as mock

from recording.recording_model import *
from recording.recording_router import *
from recording.recording_service_graphdb import RecordingServiceGraphDB


class TestRecordingRouterGet(unittest.TestCase):

    @mock.patch.object(RecordingServiceGraphDB, 'get_recording')
    def test_get_recording_without_error(self, get_recording_mock):
        dataset_name = "neo4j"
        recording_id = 1
        get_recording_mock.return_value = RecordingOut(id=recording_id)
        response = Response()
        recording_router = RecordingRouter()

        result = asyncio.run(recording_router.get_recording(recording_id, response, dataset_name))

        self.assertEqual(result, RecordingOut(id=recording_id, links=get_links(router)))

        get_recording_mock.assert_called_once_with(recording_id,dataset_name, 0)

        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RecordingServiceGraphDB, 'get_recording')
    def test_get_recording_with_error(self, get_recording_mock):
        dataset_name = "neo4j"
        get_recording_mock.return_value = RecordingOut(errors={'errors': ['test']})
        response = Response()
        recording_id = 1
        recording_router = RecordingRouter()

        result = asyncio.run(recording_router.get_recording(recording_id, response, dataset_name))

        self.assertEqual(result, RecordingOut(errors={'errors': ['test']},
                                              links=get_links(router)))
        get_recording_mock.assert_called_once_with(recording_id,dataset_name, 0)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(RecordingServiceGraphDB, 'get_recordings')
    def test_get_recordings_without_error(self, get_recordings_mock):
        dataset_name = "neo4j"
        get_recordings_mock.return_value = RecordingsOut(recordings=[
            BasicRecordingOut(id=1),
            BasicRecordingOut(id=2)])
        response = Response()
        recording_router = RecordingRouter()

        result = asyncio.run(recording_router.get_recordings(response, dataset_name))

        self.assertEqual(result, RecordingsOut(recordings=[
            BasicRecordingOut(id=1),
            BasicRecordingOut(id=2)],
            links=get_links(router)))
        get_recordings_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
