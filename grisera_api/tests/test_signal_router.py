import asyncio
import unittest
import unittest.mock as mock

from signal_node.signal_router import *


def return_signal(*args, **kwargs):
    signal_out = SignalOut(id=1, type="Epoch")
    return signal_out


class TestSignalRouter(unittest.TestCase):

    @mock.patch.object(SignalService, 'save_signal')
    def test_create_signal_without_error(self, save_signal_mock):
        save_signal_mock.side_effect = return_signal
        response = Response()
        signal = SignalIn(id=1, type="Epoch")
        signal_router = SignalRouter()

        result = asyncio.run(signal_router.create_signal(signal, response))

        self.assertEqual(result, SignalOut(id=1, type="Epoch", links=get_links(router)))
        save_signal_mock.assert_called_once_with(signal)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(SignalService, 'save_signal')
    def test_create_signal_with_error(self, save_signal_mock):
        save_signal_mock.return_value = SignalOut(type="Epoch", errors={'errors': ['test']})
        response = Response()
        signal = SignalIn(id=1, type="Epoch")
        signal_router = SignalRouter()

        result = asyncio.run(signal_router.create_signal(signal, response))

        self.assertEqual(result, SignalOut(type="Epoch", errors={'errors': ['test']}, links=get_links(router)))
        save_signal_mock.assert_called_once_with(signal)
        self.assertEqual(response.status_code, 422)
