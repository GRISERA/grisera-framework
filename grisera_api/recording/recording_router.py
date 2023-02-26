from typing import Union

from fastapi import Response
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from hateoas import get_links
from models.not_found_model import NotFoundByIdModel
from recording.recording_model import RecordingPropertyIn, RecordingRelationIn, RecordingIn, RecordingOut, RecordingsOut
from recording.recording_service import RecordingService
from services import Services

router = InferringRouter()


@cbv(router)
class RecordingRouter:
    """
    Class for routing recording based requests

    Attributes:
        recording_service (RecordingService): Service instance for recording
    """

    def __init__(self):
        self.recording_service = Services().recording_service()

    @router.post("/recordings", tags=["recordings"], response_model=RecordingOut)
    async def create_recording(self, recording: RecordingIn, response: Response, database_name: str):
        """
        Create Recording in database
        """
        create_response = self.recording_service.save_recording(recording, database_name)
        if create_response.errors is not None:
            response.status_code = 422

        # add links from hateoas
        create_response.links = get_links(router)

        return create_response

    @router.get("/recordings", tags=["recordings"], response_model=RecordingsOut)
    async def get_recordings(self, response: Response, database_name: str):
        """
        Get recordingss from database
        """

        get_response = self.recording_service.get_recordings(database_name)

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.get("/recordings/{recording_id}", tags=["recordings"],
                response_model=Union[RecordingOut, NotFoundByIdModel])
    async def get_recording(self, recording_id: int, response: Response, database_name: str):
        """
        Get recordings from database
        """

        get_response = self.recording_service.get_recording(recording_id, database_name)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.delete("/recordings/{recording_id}", tags=["recordings"],
                   response_model=Union[RecordingOut, NotFoundByIdModel])
    async def delete_recording(self, recording_id: int, response: Response, database_name: str):
        """
        Delete recordings from database
        """
        get_response = self.recording_service.delete_recording(recording_id, database_name)
        if get_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        get_response.links = get_links(router)

        return get_response

    @router.put("/recordings/{recording_id}", tags=["recordings"],
                response_model=Union[RecordingOut, NotFoundByIdModel])
    async def update_recording(self, recording_id: int, recording: RecordingPropertyIn, response: Response, database_name: str):
        """
        Update recording model in database
        """
        update_response = self.recording_service.update_recording(recording_id, recording, database_name)
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
    
    @router.put("/recordings/{recording_id}/relationships", tags=["recordings"],
                response_model=Union[RecordingOut, NotFoundByIdModel])
    async def update_recording_relationships(self, recording_id: int, recording: RecordingRelationIn, response: Response, database_name: str):
        """
        Update recordings relations in database
        """
        update_response = self.recording_service.update_recording_relationships(recording_id, recording, database_name)
        if update_response.errors is not None:
            response.status_code = 404

        # add links from hateoas
        update_response.links = get_links(router)

        return update_response
