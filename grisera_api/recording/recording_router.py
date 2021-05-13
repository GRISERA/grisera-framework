from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from recording.recording_model import RecordingsIn, RecordingsOut
from recording.recording_service import RecordingService

router = InferringRouter()


@cbv(router)
class RecordingRouter:
    """
    Class for routing recording based requests

    Attributes:
        recording_service (RecordingService): Service instance for recordings
    """
    recording_service = RecordingService()

    @router.post("/recordings", tags=["recordings"], response_model=RecordingsOut)
    async def create_recordings(self, recordings: RecordingsIn, response: Response):
        """
        Create recordings in database
        """
        create_response = self.recording_service.save_recordings(recordings)

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
