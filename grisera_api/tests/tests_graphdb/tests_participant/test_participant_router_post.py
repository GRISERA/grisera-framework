import asyncio
import unittest
import unittest.mock as mock

from participant.participant_router import *
from participant.participant_service_graphdb import ParticipantServiceGraphDB


class TestParticipantRouterPost(unittest.TestCase):

    @mock.patch.object(ParticipantServiceGraphDB, 'save_participant')
    def test_create_participant_without_error(self, save_participant_mock):
        dataset_name = "neo4j"
        save_participant_mock.return_value = ParticipantOut(name="Test Test", sex='male', id=1)
        response = Response()
        participant = ParticipantIn(name="Test Test", sex='male')
        participant_router = ParticipantRouter()

        result = asyncio.run(participant_router.create_participant(participant, response, dataset_name))

        self.assertEqual(result, ParticipantOut(name="Test Test", sex='male', id=1, links=get_links(router)))
        save_participant_mock.assert_called_once_with(participant, dataset_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipantServiceGraphDB, 'save_participant')
    def test_create_participant_with_error(self, save_participant_mock):
        dataset_name = "neo4j"
        save_participant_mock.return_value = ParticipantOut(name="Test Test", sex='male', id=1,
                                                            errors={'errors': ['test']})
        response = Response()
        participant = ParticipantIn(name="Test Test", sex='male', identifier=5)
        participant_router = ParticipantRouter()

        result = asyncio.run(participant_router.create_participant(participant, response, dataset_name))

        self.assertEqual(result, ParticipantOut(name="Test Test", sex='male', id=1, errors={'errors': ['test']},
                                                links=get_links(router)))
        save_participant_mock.assert_called_once_with(participant, dataset_name)
        self.assertEqual(response.status_code, 422)
