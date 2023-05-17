import mongomock

from modality.modality_model import ModalityIn
from observable_information.observable_information_model import ObservableInformationIn
from tests.tests_mongodb.utils import MongoTestCase
from models.not_found_model import NotFoundByIdModel
from services import Services
from mongo_service.mongodb_api_config import mongo_api_host, mongo_api_port
from recording.recording_model import RecordingIn


class TestMongoRegisteredData(MongoTestCase):
    def generate_recording(self, save: bool):
        recording = RecordingIn()
        if not save:
            return recording
        service = Services().recording_service()
        return service.save_recording(recording)
    
    def generate_modality(self, save: bool):
        modality = ModalityIn(modality="A modality")
        if not save:
            return modality
        service = Services().modality_service()
        return service.save_modality(modality)

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_create(self):
        service = Services().observable_information_service()
        recording = self.generate_recording(save=True)
        observable_information = ObservableInformationIn(recording_id=recording.id)
        created_oi = service.save_observable_information(observable_information)
        self.assertEqual(created_oi.recording_id, recording.id)

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_get(self):
        service = Services().observable_information_service()
        recording = self.generate_recording(save=True)
        observable_information = ObservableInformationIn(recording_id=recording.id)
        created_oi = service.save_observable_information(observable_information)
        fetched_oi = service.get_observable_information(created_oi.id)
        self.assertFalse(type(fetched_oi) is NotFoundByIdModel)
        self.assertEqual(fetched_oi.recording_id, recording.id)

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_delete(self):
        service = Services().observable_information_service()

        recording = self.generate_recording(save=True)
        observable_information = ObservableInformationIn(recording_id=recording.id)
        created_oi = service.save_observable_information(observable_information)
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
        modality = self.generate_modality(save=True)
        observable_information = ObservableInformationIn(recording_id=recording.id, modality_id=modality.id)
        created_oi = service.save_observable_information(observable_information)

        fetched_oi = service.get_observable_information(created_oi.id, depth=1)
        self.assertFalse(type(fetched_oi) is NotFoundByIdModel)
        self.assertEqual(fetched_oi.recording.id, recording.id)
        self.assertEqual(fetched_oi.modality.id, modality.id)
        self.assertEqual(fetched_oi.modality.modality, modality.modality)
