from recording.recording_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_recording(*args, **kwargs):
    return RecordingOut(id=1, participation_id=3, registered_channel_id=2)


class TestRecordingPost(unittest.TestCase):

    @mock.patch.object(RecordingService, 'save_recording')
    def test_recording_post_without_error(self, mock_service):
        mock_service.side_effect = return_recording
        response = Response()
        recording = RecordingIn(participation_id=3, registered_channel_id=2)
        recording_router = RecordingRouter()

        result = asyncio.run(recording_router.create_recording(recording, response))

        self.assertEqual(result, RecordingOut(participation_id=3, registered_channel_id=2, id=1, links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RecordingService, 'save_recording')
    def test_recording_post_with_error(self, mock_service):
        mock_service.return_value = RecordingOut(participation_id=3, registered_channel_id=2, errors={'errors': ['test']})
        response = Response()
        recording = RecordingIn(participation_id=3, registered_channel_id=2)
        recording_router = RecordingRouter()

        result = asyncio.run(recording_router.create_recording(recording, response))

        self.assertEqual(response.status_code, 422)
