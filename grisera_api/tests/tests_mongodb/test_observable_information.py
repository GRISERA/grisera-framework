import mongomock

from observable_information.observable_information_model import ObservableInformationIn
from registered_channel.registered_channel_model import RegisteredChannelIn
from tests.tests_mongodb.utils import MongoTestCase
from models.not_found_model import NotFoundByIdModel
from services import Services
from registered_data.registered_data_model import RegisteredDataIn
from mongo_service.mongodb_api_config import mongo_api_host, mongo_api_port
from recording.recording_model import RecordingIn


class TestMongoRegisteredData(MongoTestCase):
    def generate_recording(self, save: bool):
        recording = RecordingIn()
        if not save:
            return recording
        service = Services().recording_service()
        return service.save_recording(recording)

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_create(self):
        service = Services().observable_information_service()
        recording = self.generate_recording(save=True)
        observable_infromation = ObservableInformationIn(recording_id=recording.id)
        created_oi = service.save_observable_information(observable_infromation)
        self.assertEqual(created_oi.recording_id, recording.id)

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_get(self):
        service = Services().observable_information_service()
        recording = self.generate_recording(save=True)
        observable_infromation = ObservableInformationIn(recording_id=recording.id)
        created_oi = service.save_observable_information(observable_infromation)
        fetched_oi = service.get_observable_information(created_oi.id)
        self.assertFalse(type(fetched_oi) is NotFoundByIdModel)
        self.assertEqual(fetched_oi.recording_id, recording.id)

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_delete(self):
        service = Services().observable_information_service()

        recording = self.generate_recording(save=True)
        observable_infromation = ObservableInformationIn(recording_id=recording.id)
        created_oi = service.save_observable_information(observable_infromation)
        other_oi = service.save_observable_information(
            ObservableInformationIn(recording_id=recording.id)
        )
        service.delete_observable_information(created_oi.id)

        get_result = service.get_observable_information(created_oi.id)
        self.assertTrue(type(get_result) is NotFoundByIdModel)
        # check wether other oi related to this recording wasn't deleted
        get_other_result = service.get_observable_information(other_oi.id)
        self.assertFalse(type(get_other_result) is NotFoundByIdModel)

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_traverse_one(self):
        service = Services().observable_information_service()

        recording = self.generate_recording(save=True)
        observable_infromation = ObservableInformationIn(recording_id=recording.id)
        created_oi = service.save_observable_information(observable_infromation)

        fetched_oi = service.get_observable_information(created_oi.id, depth=1)
        self.assertFalse(type(fetched_oi) is NotFoundByIdModel)
        self.assertEqual(fetched_oi.recording.id, recording.id)
