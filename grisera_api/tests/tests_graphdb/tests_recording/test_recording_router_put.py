import asyncio
import unittest
import unittest.mock as mock

from recording.recording_router import *
from recording.recording_service_graphdb import RecordingServiceGraphDB


class TestRecordingRouterPut(unittest.TestCase):

    @mock.patch.object(RecordingServiceGraphDB, 'update_recording_relationships')
    def test_update_recording_relationships_without_error(self, update_recording_relationships_mock):
        database_name = "neo4j"
        id_node = 1
        update_recording_relationships_mock.return_value = RecordingOut(id=id_node)
        response = Response()
        recording_in = RecordingIn(participation_id=2, registered_channel_id=3)
        recording_out = RecordingOut(id=id_node, links=get_links(router))
        recording_router = RecordingRouter()

        result = asyncio.run(recording_router.
                             update_recording_relationships(id_node, recording_in, response, database_name))

        self.assertEqual(result, recording_out)
        update_recording_relationships_mock.assert_called_once_with(id_node, recording_in, database_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RecordingServiceGraphDB, 'update_recording_relationships')
    def test_update_recording_relationships_with_error(self, update_recording_relationships_mock):
        database_name = "neo4j"
        id_node = 1
        update_recording_relationships_mock.return_value = RecordingOut(id=id_node, errors="error")
        response = Response()
        recording_in = RecordingIn(participation_id=2, registered_channel_id=3)
        recording_out = RecordingOut(id=id_node, errors="error", links=get_links(router))
        recording_router = RecordingRouter()

        result = asyncio.run(recording_router.
                             update_recording_relationships(id_node, recording_in, response, database_name))

        self.assertEqual(result, recording_out)
        update_recording_relationships_mock.assert_called_once_with(id_node, recording_in, database_name)
        self.assertEqual(response.status_code, 404)