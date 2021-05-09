from observable_information.observable_information_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_observable_information(*args, **kwargs):
    observable_information_out = ObservableInformationOut(modality="body posture",
                                                          live_activity="muscles activity", id=1)
    return observable_information_out


class TestObservableInformationPost(unittest.TestCase):

    @mock.patch.object(ObservableInformationService, 'save_observable_information')
    def test_observable_information_post_without_error(self, mock_service):
        mock_service.side_effect = return_observable_information
        response = Response()
        observable_information = ObservableInformationIn(modality="body posture", live_activity="muscles activity")
        observable_information_router = ObservableInformationRouter()

        result = asyncio.run(observable_information_router
                             .create_observable_information(observable_information, response))

        self.assertEqual(result, ObservableInformationOut(modality="body posture", live_activity="muscles activity",
                                                          id=1, links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(ObservableInformationService, 'save_observable_information')
    def test_observable_information_post_with_error(self, mock_service):
        mock_service.return_value = ObservableInformationOut(modality="body posture", live_activity="muscles activity",
                                                             errors={'errors': ['test']})
        response = Response()
        observable_information = ObservableInformationIn(modality="body posture", live_activity="muscles activity")
        observable_information_router = ObservableInformationRouter()

        result = asyncio.run(observable_information_router
                             .create_observable_information(observable_information, response))

        self.assertEqual(response.status_code, 422)
