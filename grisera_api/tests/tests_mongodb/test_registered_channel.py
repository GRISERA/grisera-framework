import mongomock

from services import Services
from tests.tests_mongodb.utils import MongoTestCase
from models.not_found_model import NotFoundByIdModel
from recording.recording_model import RecordingIn
from registered_channel.registered_channel_model import RegisteredChannelIn
from registered_data.registered_data_model import RegisteredDataIn
from channel.channel_model import ChannelIn, Type
from mongo_service.mongodb_api_config import mongo_api_host, mongo_api_port


class TestMongoRegisteredData(MongoTestCase):
    def generate_channel(self):
        service = Services().channel_service()
        return service.save_channel(ChannelIn(type=Type.audio))

    def generate_registered_data(self):
        service = Services().registered_data_service()
        return service.save_registered_data(RegisteredDataIn(source="source"))

    def generate_registered_channel(
        self, related_channel: ChannelIn = None, related_rd: RegisteredDataIn = None
    ):
        related_channel = related_channel or self.generate_channel()
        related_rd = related_rd or self.generate_registered_data()
        return RegisteredChannelIn(
            channel_id=related_channel.id, registered_data_id=related_rd.id
        )

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_save(self):
        service = Services().registered_channel_service()
        related_channel = self.generate_channel()
        related_rd = self.generate_registered_data()
        rc = RegisteredChannelIn(
            channel_id=related_channel.id, registered_data_id=related_rd.id
        )
        created_rc = service.save_registered_channel(rc)

        self.assertEqual(created_rc.channel_id, related_channel.id)
        self.assertEqual(created_rc.registered_data_id, related_rd.id)

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_get(self):
        service = Services().registered_channel_service()
        rc = self.generate_registered_channel()
        created_rc = service.save_registered_channel(rc)
        fetched_rc = service.get_registered_channel(created_rc.id)

        self.assertEqual(created_rc.channel_id, fetched_rc.channel_id)
        self.assertEqual(created_rc.registered_data_id, fetched_rc.registered_data_id)

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_update_relationships(self):
        service = Services().registered_channel_service()
        rc = self.generate_registered_channel()
        created_rc = service.save_registered_channel(rc)

        new_related_channel = self.generate_channel()
        updated_rc = self.generate_registered_channel(new_related_channel)
        service.update_registered_channel_relationships(created_rc.id, updated_rc)
        fetched_rc = service.get_registered_channel(created_rc.id)

        self.assertEqual(fetched_rc.channel_id, new_related_channel.id)

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_delete(self):
        service = Services().registered_channel_service()
        rc = self.generate_registered_channel()
        created_rc = service.save_registered_channel(rc)

        service.delete_registered_channel(created_rc.id)
        get_result = service.get_registered_channel(created_rc.id)
        self.assertTrue(type(get_result) is NotFoundByIdModel)

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_traverse_one(self):
        service = Services().registered_channel_service()
        registered_data_service = Services().registered_data_service()
        channel_service = Services().channel_service()
        recording_service = Services().recording_service()

        rc = self.generate_registered_channel()
        created_rc = service.save_registered_channel(rc)
        recordings_count = 10
        created_recordings = []
        for _ in range(recordings_count):
            recording = RecordingIn(registered_channel_id=created_rc.id)
            created_recording = recording_service.save_recording(recording)
            created_recordings.append(created_recording)

        # create registered channels related to other channel
        other_rd = service.save_registered_channel(self.generate_registered_channel())
        for _ in range(5):
            unrelated_recording = RecordingIn(registered_channel_id=other_rd.id)
            recording_service.save_recording(unrelated_recording)

        result = service.get_registered_channel(created_rc.id, depth=1)
        self.assertFalse(type(result) is NotFoundByIdModel)
        self.assertEqual(len(result.recordings), recordings_count)
        expected_created_ids = {recording.id for recording in created_recordings}
        created_ids = {recording.id for recording in result.recordings}
        self.assertSetEqual(expected_created_ids, created_ids)
