from graph_api_service import GraphApiService
from author.author_model import AuthorIn, AuthorOut


class AuthorService:
    """
    Object to handle logic of authors requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
    """
    graph_api_service = GraphApiService()

    def save_author(self, author: AuthorIn):
        """
        Send request to graph api to create new author

        Args:
            author (AuthorIn): Author to be added

        Returns:
            Result of request as author object
        """
        node_response = self.graph_api_service.create_node("Author")

        if node_response["errors"] is not None:
            return AuthorOut(name=author.name, errors=node_response["errors"])

        author_id = node_response["id"]
        properties_response = self.graph_api_service.create_properties(author_id, author)
        if properties_response["errors"] is not None:
            return AuthorOut(name=author.name, errors=properties_response["errors"])

        return AuthorOut(name=author.name, institution=author.institution, id=author_id)
