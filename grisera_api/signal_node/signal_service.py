from graph_api_service import GraphApiService
from signal_node.signal_model import SignalIn, SignalOut


class SignalService:
    """
    Object to handle logic of signals requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_signal(self, signal: SignalIn):
        """
        Send request to graph api to create new signal

        Args:
            signal (SignalIn): Signal to be added

        Returns:
            Result of request as signal object
        """
        node_response_signal = self.graph_api_service.create_node("Signal")

        if node_response_signal["errors"] is not None:
            return SignalOut(type=signal.type, source=signal.source,
                             observable_information_id=signal.observable_information_id,
                             recording_id=signal.recording_id,
                             additional_properties=signal.additional_properties,
                             errors=node_response_signal["errors"])

        signal_id = node_response_signal["id"]
        properties_response = self.graph_api_service.create_properties(signal_id, signal)
        if properties_response["errors"] is not None:
            return SignalOut(type=signal.type, source=signal.source,
                             observable_information_id=signal.observable_information_id,
                             recording_id=signal.recording_id,
                             additional_properties=signal.additional_properties,
                             errors=properties_response["errors"])

        self.graph_api_service.create_relationships(signal_id, signal.observable_information_id,
                                                    "hasObservableInformation")
        self.graph_api_service.create_relationships(signal_id, signal.recording_id,
                                                    "hasRecording")

        return SignalOut(type=signal.type, source=signal.source,
                         observable_information_id=signal.observable_information_id,
                         recording_id=signal.recording_id, id=signal_id,
                         additional_properties=signal.additional_properties)
