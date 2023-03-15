import asyncio
import unittest
import unittest.mock as mock
from grisera_api.participant_state.participant_state_router import *
from grisera_api.participant_state.participant_state_service_graphdb import ParticipantStateServiceGraphDB


class TestParticipantStateRouterDelete(unittest.TestCase):

    @mock.patch.object(ParticipantStateServiceGraphDB, 'delete_participant_state')
    def test_delete_participant_state_without_error(self, delete_participant_state_mock):
        participant_state_id = 1
        delete_participant_state_mock.return_value = ParticipantStateOut(age=5, id=participant_state_id)
        response = Response()
        participant_state_router = ParticipantStateRouter()

        result = asyncio.run(participant_state_router.delete_participant_state(participant_state_id, response))

        self.assertEqual(result, ParticipantStateOut(age=5, id=participant_state_id, links=get_links(router)))
        delete_participant_state_mock.assert_called_once_with(participant_state_id)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipantStateServiceGraphDB, 'delete_participant_state')
    def test_delete_participant_state_with_error(self, delete_participant_state_mock):
        delete_participant_state_mock.return_value = ParticipantStateOut(age=5, errors={'errors': ['test']})
        response = Response()
        participant_state_id = 1
        participant_state_router = ParticipantStateRouter()

        result = asyncio.run(participant_state_router.delete_participant_state(participant_state_id, response))

        self.assertEqual(result, ParticipantStateOut(age=5, errors={'errors': ['test']}, links=get_links(router)))
        delete_participant_state_mock.assert_called_once_with(participant_state_id)
        self.assertEqual(response.status_code, 404)
