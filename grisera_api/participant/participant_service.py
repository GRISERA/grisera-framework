import requests
from graph_api_config import graph_api_address
from participant.participant_model import ParticipantIn, ParticipantOut


class ParticipantService:
    """
    Object to handle logic of participants requests
    """

    def save_participant(self, participant: ParticipantIn):
        """
        Send request to graph api to create new participant

        Args:
            participant (ParticipantIn): Participant to be added

        Returns:
            Result of request as participant object
        """
        commit_body = {"labels": ["Participant"]}
        response = requests.post(url=graph_api_address+"/nodes",
                                 json=commit_body).json()

        if response["errors"] is not None:
            return ParticipantOut(errors=response["errors"])
        participant_id = response["id"]
        return ParticipantOut(id=participant_id)
