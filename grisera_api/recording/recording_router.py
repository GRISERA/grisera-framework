from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from recording.recording_model import RecordingIn, RecordingOut
from recording.recording_service import RecordingService

router = InferringRouter()


@cbv(router)
class RecordingRouter:
    """
    Class for routing recording based requests

    Attributes:
        recording_service (RecordingService): Service instance for recording
    """
    recording_service = RecordingService()

    @router.post("/recording", tags=["recording"], response_model=RecordingOut)
    async def create_recording(self, recording: RecordingIn, response: Response):
        """
        Create Recording in database
        """
        create_response = self.recording_service.save_recording(recording)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response
