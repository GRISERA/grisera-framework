import asyncio
import unittest
import unittest.mock as mock

from author.author_model import AuthorIn
from publication.publication_router import *


class TestPublicationRouter(unittest.TestCase):

    @mock.patch.object(PublicationService, 'save_publication')
    def test_create_publication_without_error(self, save_publication_mock):
        response = Response()
        authors = [AuthorIn(name='TestName'), AuthorIn(name='TestName')]
        publication = PublicationIn(title='Test', authors=authors)
        save_publication_mock.return_value = PublicationOut(title='Test', authors=authors)
        publication_router = PublicationRouter()

        result = asyncio.run(publication_router.create_publication(publication, response))

        self.assertEqual(result, PublicationOut(title='Test', authors=authors, links=get_links(router)))
        save_publication_mock.assert_called_once_with(publication)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(PublicationService, 'save_publication')
    def test_create_publication_with_error(self, save_publication_mock):
        authors = [AuthorIn(name='TestName'), AuthorIn(name='TestName')]
        save_publication_mock.return_value = PublicationOut(title='Test', authors=authors, errors={'errors': ['test']})
        response = Response()
        publication = PublicationIn(title='Test', authors=authors)
        publication_router = PublicationRouter()

        result = asyncio.run(publication_router.create_publication(publication, response))

        self.assertEqual(result, PublicationOut(title='Test', authors=authors, errors={'errors': ['test']}, links=get_links(router)))
        save_publication_mock.assert_called_once_with(publication)
        self.assertEqual(response.status_code, 422)
