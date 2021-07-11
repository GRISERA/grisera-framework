from recording.recording_router import *
import unittest
import unittest.mock as mock
import asyncio


class TestRecordingRouter(unittest.TestCase):

    @mock.patch.object(RecordingService, 'save_recording')
    def test_create_recording_without_error(self, save_recording_mock):
        save_recording_mock.return_value = RecordingOut(participation_id=3, registered_channel_id=2, id=1)
        response = Response()
        recording = RecordingIn(participation_id=3, registered_channel_id=2)
        recording_router = RecordingRouter()

        result = asyncio.run(recording_router.create_recording(recording, response))

        self.assertEqual(result, RecordingOut(participation_id=3, registered_channel_id=2, id=1,
                                              links=get_links(router)))
        save_recording_mock.assert_called_once_with(recording)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(RecordingService, 'save_recording')
    def test_create_recording_with_error(self, save_recording_mock):
        save_recording_mock.return_value = RecordingOut(participation_id=3, registered_channel_id=2, id=1,
                                                       errors={'errors': ['test']})
        response = Response()
        recording = RecordingIn(participation_id=3, registered_channel_id=2)
        recording_router = RecordingRouter()

        result = asyncio.run(recording_router.create_recording(recording, response))

        self.assertEqual(result, RecordingOut(participation_id=3, registered_channel_id=2, id=1,
                                              errors={'errors': ['test']}, links=get_links(router)))
        save_recording_mock.assert_called_once_with(recording)
        self.assertEqual(response.status_code, 422)
