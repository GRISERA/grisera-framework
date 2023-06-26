import mongomock
from tests.tests_mongodb.utils import MongoTestCase

from recording.recording_model import RecordingIn
from models.not_found_model import NotFoundByIdModel
from services import Services
from channel.channel_model import ChannelIn, Type
from registered_channel.registered_channel_model import RegisteredChannelIn
from mongo_service.mongodb_api_config import mongo_api_host, mongo_api_port


class TestMongoChannel(MongoTestCase):
    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_save(self):
        channel_service = Services().channel_service()
        channel = ChannelIn(type=Type.audio)
        created_channel = channel_service.save_channel(channel)

        self.assertEqual(created_channel.type, channel.type)

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_get(self):
        channel_service = Services().channel_service()
        channel = ChannelIn(type=Type.audio)
        created_channel = channel_service.save_channel(channel)
        fetched_channel = channel_service.get_channel(created_channel.id)

        self.assertEqual(created_channel.type, fetched_channel.type)

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_get_many(self):
        channel_service = Services().channel_service()
        channel = ChannelIn(type=Type.audio)
        created_channel = channel_service.save_channel(channel)
        result = channel_service.get_channels()
        fetched_channels_ids = [channel.id for channel in result.channels]

        self.assertIn(created_channel.id, fetched_channels_ids)

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_traverse_one(self):
        channel_service = Services().channel_service()
        registered_channel_service = Services().registered_channel_service()

        channel = ChannelIn(type=Type.audio)
        created_channel = channel_service.save_channel(channel)
        registered_channels_count = 10
        created_registered_channels = []
        for _ in range(registered_channels_count):
            registered_channel = RegisteredChannelIn(channel_id=created_channel.id)
            created_rc = registered_channel_service.save_registered_channel(
                registered_channel
            )
            created_registered_channels.append(created_rc)

        # create registered channels related to other channel
        other_channel = channel_service.save_channel(ChannelIn(type=Type.audio))
        for _ in range(5):
            unrelated_registered_channel = RegisteredChannelIn(
                channel_id=other_channel.id
            )
            registered_channel_service.save_registered_channel(
                unrelated_registered_channel
            )
        result = channel_service.get_channel(created_channel.id, depth=1)

        self.assertFalse(type(result) is NotFoundByIdModel)
        self.assertEqual(len(result.registered_channels), registered_channels_count)
        expected_created_ids = {rc.id for rc in created_registered_channels}
        created_ids = {rc.id for rc in result.registered_channels}
        self.assertSetEqual(expected_created_ids, created_ids)
        # check whether too much models weren't fetched
        self.assertIsNone(result.registered_channels[0].channel)
        self.assertIsNone(result.registered_channels[0].recordings)

    @mongomock.patch(servers=((mongo_api_host, mongo_api_port),))
    def test_traverse_two(self):
        channel_service = Services().channel_service()
        channel = ChannelIn(type=Type.audio)
        created_channel = channel_service.save_channel(channel)

        registered_channel = RegisteredChannelIn(channel_id=created_channel.id)
        created_rc = (
            Services()
            .registered_channel_service()
            .save_registered_channel(registered_channel)
        )

        recordings_count = 3
        for _ in range(recordings_count):
            recording = RecordingIn(registered_channel_id=created_rc.id)
            Services().recording_service().save_recording(recording)

        result = channel_service.get_channel(created_channel.id, depth=2)
        self.assertFalse(type(result) is NotFoundByIdModel)
        self.assertEqual(len(result.registered_channels), 1)
        self.assertFalse(result.registered_channels[0].recordings is None)
        self.assertEqual(
            len(result.registered_channels[0].recordings), recordings_count
        )
