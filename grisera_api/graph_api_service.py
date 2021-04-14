import requests
from graph_api_config import graph_api_address
from participant.participant_model import ParticipantIn


class GraphApiService:
    """
    Object that handles communication with graph api

    Attributes:
        graph_api_url (str): Graph API URL
    """
    graph_api_url = graph_api_address

    def post(self, url_part, request_body):
        """
        Send request post to Graph API

        Args:
            url_part (str): Part to add at the end of url
            request_body (dict): Body of request

        Returns:
            Result of request
        """

        response = requests.post(url=self.graph_api_url+url_part,
                                 json=request_body).json()
        return response

    def create_participant_node(self):
        """
        Send to the Graph API request to create participant node

        Returns:
            Result of request
        """
        request_body = {"labels": ["Participant"]}
        return self.post("/nodes", request_body)

    def create_participant_properties(self, participant_id: int, participant: ParticipantIn):
        """
        Send to the Graph API request to create properties for participant

        Args:
            participant_id (int): Id of participant
            participant (ParticipantIn): Participant to be created

        Returns:
            Result of request
        """
        request_body = []
        for property in participant.dict().items():
            if property[1] is not None:
                request_body.append({"key": property[0], "value": property[1]})

        return self.post("/nodes/{}/properties".format(participant_id), request_body)
