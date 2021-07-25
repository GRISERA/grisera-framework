from graph_api_service import GraphApiService
from publication.publication_model import PublicationIn, PublicationOut
from author.author_service import AuthorService


class PublicationService:
    """
    Object to handle logic of publications requests

    Attributes:
        graph_api_service (GraphApiService): Service used to communicate with Graph API
        author_service (AuthorService): Service used to communicate with Author
    """
    graph_api_service = GraphApiService()
    author_service = AuthorService()

    def save_publication(self, publication: PublicationIn):
        """
        Send request to graph api to create new publication

        Args:
            publication (PublicationIn): Publication to be added

        Returns:
            Result of request as publication object
        """
        node_response_publication = self.graph_api_service.create_node("Publication")

        if node_response_publication["errors"] is not None:
            return PublicationOut(title=publication.title, authors=publication.authors,
                                  errors=node_response_publication["errors"])

        publication_id = node_response_publication["id"]
        properties_response = self.graph_api_service.create_properties(publication_id, publication)
        if properties_response["errors"] is not None:
            return PublicationOut(title=publication.title, authors=publication.authors,
                                  errors=properties_response["errors"])

        # Create Nodes Author for publication
        authors_out = []
        for author in publication.authors:
            node_response_author = self.author_service.save_author(author=author)
            # Create relationship between Author and Publication
            relationship_response_publication_author = self.graph_api_service.create_relationships(
                end_node=node_response_author.id, start_node=publication_id, name="hasAuthor")
            if relationship_response_publication_author["errors"] is not None:
                return PublicationOut(title=publication.title, authors=publication.authors,
                                      errors=relationship_response_publication_author["errors"])
            authors_out.append(node_response_author)

        return PublicationOut(title=publication.title, authors=authors_out, id=publication_id)
