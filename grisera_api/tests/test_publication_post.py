from publication.publication_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_publication(*args, **kwargs):
    publication_out = PublicationOut(id=1, title="test", authors=args[0].authors)
    return publication_out


class TestPublicationPost(unittest.TestCase):

    @mock.patch.object(PublicationService, 'save_publication')
    def test_publication_post_without_error(self, mock_service):
        mock_service.side_effect = return_publication
        response = Response()
        publication = PublicationIn(title="test", authors=[{"name": "Testowa", "institution": "TestowaInst"}])
        publication_router = PublicationRouter()

        result = asyncio.run(publication_router.create_publication(publication, response))

        self.assertEqual(result, PublicationOut(id=1, title="test",
                                                authors=[{"name": "Testowa", "institution": "TestowaInst"}],
                                                links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(PublicationService, 'save_publication')
    def test_publication_post_with_error(self, mock_service):
        mock_service.return_value = PublicationOut(title="test",
                                                   authors=[{"name": "Testowa", "institution": "TestowaInst"}],
                                                   errors={'errors': ['test']})
        response = Response()
        publication = PublicationIn(title="test", authors=[{"name": "Testowa", "institution": "TestowaInst"}])
        publication_router = PublicationRouter()

        result = asyncio.run(publication_router.create_publication(publication, response))

        self.assertEqual(response.status_code, 422)
