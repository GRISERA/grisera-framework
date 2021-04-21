from author.author_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_author(*args, **kwargs):
    author_out = AuthorOut(id=1, name="test")
    return author_out


class TestAuthorPost(unittest.TestCase):

    @mock.patch.object(AuthorService, 'save_author')
    def test_author_post_without_error(self, mock_service):
        mock_service.side_effect = return_author
        response = Response()
        author = AuthorIn(name="test")
        author_router = AuthorRouter()

        result = asyncio.run(author_router.create_author(author, response))

        self.assertEqual(result, AuthorOut(id=1, name="test", links=get_links(router)))
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(AuthorService, 'save_author')
    def test_author_post_with_error(self, mock_service):
        mock_service.return_value = AuthorOut(name="test", errors={'errors': ['test']})
        response = Response()
        author = AuthorIn(name="test")
        author_router = AuthorRouter()

        result = asyncio.run(author_router.create_author(author, response))

        self.assertEqual(response.status_code, 422)
