import asyncio
import unittest
import unittest.mock as mock

from participant.participant_model import ParticipantIn
from participant_state.participant_state_router import *
from participant_state.participant_state_service_graphdb import ParticipantStateServiceGraphDB


class TestParticipantStateRouterPost(unittest.TestCase):

    @mock.patch.object(ParticipantStateServiceGraphDB, 'save_participant_state')
    def test_create_participant_state_without_error(self, save_participant_state_mock):
        dataset_name = "neo4j"
        save_participant_state_mock.return_value = ParticipantStateOut(
            participant=ParticipantIn(name="Test Test", sex='male', identifier=5), id=1)
        response = Response()
        participant_state = ParticipantStateIn(participant=ParticipantIn(name="Test Test", sex='male',
                                                                         identifier=5))
        participant_state_router = ParticipantStateRouter()

        result = asyncio.run(participant_state_router.create_participant_state(participant_state, response, dataset_name))

        self.assertEqual(result, ParticipantStateOut(participant=ParticipantIn(name="Test Test", sex='male',
                                                                               identifier=5),
                                                     id=1, links=get_links(router)))
        save_participant_state_mock.assert_called_once_with(participant_state, dataset_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipantStateServiceGraphDB, 'save_participant_state')
    def test_create_participant_state_with_error(self, save_participant_state_mock):
        dataset_name = "neo4j"
        save_participant_state_mock.return_value = ParticipantStateOut(
            participant=ParticipantIn(name="Test Test", sex='male', identifier=5), errors={'errors': ['test']})
        response = Response()
        participant_state = ParticipantStateIn(participant=ParticipantIn(name="Test Test", sex='male',
                                                                         identifier=5))
        participant_state_router = ParticipantStateRouter()

        result = asyncio.run(participant_state_router.create_participant_state(participant_state, response, dataset_name))

        self.assertEqual(result, ParticipantStateOut(participant=ParticipantIn(name="Test Test", sex='male',
                                                                               identifier=5),
                                                     errors={'errors': ['test']}, links=get_links(router)))
        save_participant_state_mock.assert_called_once_with(participant_state, dataset_name)
        self.assertEqual(response.status_code, 422)
