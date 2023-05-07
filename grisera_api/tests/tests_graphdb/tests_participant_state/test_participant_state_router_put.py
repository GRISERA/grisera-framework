import asyncio
import unittest
import unittest.mock as mock
from participant_state.participant_state_router import *
from participant_state.participant_state_service_graphdb import ParticipantStateServiceGraphDB


class TestParticipantStateRouterPut(unittest.TestCase):

    @mock.patch.object(ParticipantStateServiceGraphDB, 'update_participant_state')
    def test_update_participant_state_without_error(self, update_participant_state_mock):
        dataset_name = "neo4j"
        participant_state_id = 1
        update_participant_state_mock.return_value = ParticipantStateOut(age=5, id=participant_state_id)
        response = Response()
        participant_state = ParticipantStatePropertyIn(age=5)
        participant_state_router = ParticipantStateRouter()

        result = asyncio.run(participant_state_router.update_participant_state(
            participant_state_id, participant_state, response, dataset_name))

        self.assertEqual(result, ParticipantStateOut(age=5, id=participant_state_id, links=get_links(router)))
        update_participant_state_mock.assert_called_once_with(participant_state_id, participant_state, dataset_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipantStateServiceGraphDB, 'update_participant_state')
    def test_update_participant_state_with_error(self, update_participant_state_mock):
        dataset_name = "neo4j"
        participant_state_id = 1
        update_participant_state_mock.return_value = ParticipantStateOut(age=5, errors={'errors': ['test']})
        response = Response()
        participant_state = ParticipantStatePropertyIn(age=5)
        participant_state_router = ParticipantStateRouter()

        result = asyncio.run(participant_state_router.update_participant_state(
            participant_state_id, participant_state, response, dataset_name))

        self.assertEqual(result, ParticipantStateOut(age=5, errors={'errors': ['test']},
                                                             links=get_links(router)))
        update_participant_state_mock.assert_called_once_with(participant_state_id, participant_state, dataset_name)
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(ParticipantStateServiceGraphDB, 'update_participant_state_relationships')
    def test_update_participant_state_relationships_without_error(self, update_participant_state_relationships_mock):
        dataset_name = "neo4j"
        id_node = 1
        update_participant_state_relationships_mock.return_value = ParticipantStateOut(age=5, id=id_node)
        response = Response()
        participant_state_in = ParticipantStateRelationIn(participant_id=2, personality_id=3, appearance_id=4)
        participant_state_out = ParticipantStateOut(age=5, id=id_node, links=get_links(router))
        participant_state_router = ParticipantStateRouter()

        result = asyncio.run(participant_state_router.
                             update_participant_state_relationships(id_node, participant_state_in, response, dataset_name))

        self.assertEqual(result, participant_state_out)
        update_participant_state_relationships_mock.assert_called_once_with(id_node, participant_state_in, dataset_name)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ParticipantStateServiceGraphDB, 'update_participant_state_relationships')
    def test_update_participant_state_relationships_with_error(self, update_participant_state_relationships_mock):
        dataset_name = "neo4j"
        id_node = 1
        update_participant_state_relationships_mock.return_value = ParticipantStateOut(age=5, id=id_node, errors="error")
        response = Response()
        participant_state_in = ParticipantStateRelationIn(participant_id=2, personality_id=3, appearance_id=4)
        participant_state_out = ParticipantStateOut(age=5, id=id_node, errors="error", links=get_links(router))
        participant_state_router = ParticipantStateRouter()

        result = asyncio.run(participant_state_router.
                             update_participant_state_relationships(id_node, participant_state_in, response, dataset_name))

        self.assertEqual(result, participant_state_out)
        update_participant_state_relationships_mock.assert_called_once_with(id_node, participant_state_in, dataset_name)
        self.assertEqual(response.status_code, 404)
