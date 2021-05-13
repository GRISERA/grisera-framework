from recording.recording_router import *
from recording.recording_model import *
import unittest
import unittest.mock as mock
import asyncio


def return_recordings(*args, **kwargs):
    recordings_out = RecordingsOut(recordings=[RecordingOut(activity_id=1, participant_state_id=1, id=2)])
    return recordings_out


class TestRecordingsPost(unittest.TestCase):

    @mock.patch.object(RecordingService, 'save_recordings')
    def test_recordings_post_without_error(self, mock_service):
        mock_service.side_effect = return_recordings
        response = Response()
        recordings = RecordingsIn(activities=[1], participant_state_id=1)
        recording_router = RecordingRouter()

        result = asyncio.run(recording_router.create_recordings(recordings, response))

        self.assertEqual(result, RecordingsOut(recordings=[RecordingOut(activity_id=1, participant_state_id=1, id=2)],
                                               links=get_links(router)))
        self.assertEqual(response.status_code, 200)
