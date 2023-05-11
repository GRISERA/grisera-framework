import asyncio
import unittest
import unittest.mock as mock
from participant_state.participant_state_router import *
from participant_state.participant_state_model import BasicParticipantStateOut, ParticipantStateOut
from participant_state.participant_state_service_graphdb import ParticipantStateServiceGraphDB


class TestParticipantStateRouterGet(unittest.TestCase):

    @mock.patch.object(ParticipantStateServiceGraphDB, 'get_participant_state')
    def test_get_participant_state_without_error(self, get_participant_state_mock):
        dataset_name = "neo4j"
        participant_state_id = 1
        get_participant_state_mock.return_value = ParticipantStateOut(age=5)
        response = Response()
        participant_state_router = ParticipantStateRouter()

        result = asyncio.run(participant_state_router.get_participant_state(participant_state_id, response, dataset_name))

        self.assertEqual(result, ParticipantStateOut(age=5, links=get_links(router)))
        get_participant_state_mock.assert_called_once_with(participant_state_id, dataset_name, 0)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipantStateServiceGraphDB, 'get_participant_state')
    def test_get_participant_state_with_error(self, get_participant_state_mock):
        dataset_name = "neo4j"
        get_participant_state_mock.return_value = ParticipantStateOut(age=5, errors={'errors': ['test']})
        response = Response()
        participant_state_id = 1
        participant_state_router = ParticipantStateRouter()

        result = asyncio.run(participant_state_router.get_participant_state(participant_state_id, response, dataset_name))

        self.assertEqual(result, ParticipantStateOut(age=5, errors={'errors': ['test']},
                                                     links=get_links(router)))
        get_participant_state_mock.assert_called_once_with(participant_state_id, dataset_name, 0)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(ParticipantStateServiceGraphDB, 'get_participant_states')
    def test_get_participants_state_without_error(self, get_participant_states_mock):
        dataset_name = "neo4j"
        get_participant_states_mock.return_value = ParticipantStatesOut(participant_states=[
            BasicParticipantStateOut(age=5, id=1),
            BasicParticipantStateOut(age=10, id=2)])
        response = Response()
        participant_state_router = ParticipantStateRouter()

        result = asyncio.run(participant_state_router.get_participant_states(response, dataset_name))

        self.assertEqual(result, ParticipantStatesOut(participant_states=[
            BasicParticipantStateOut(age=5, id=1),
            BasicParticipantStateOut(age=10, id=2)],
            links=get_links(router)))
        get_participant_states_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)
