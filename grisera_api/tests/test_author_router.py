from author.author_router import *
import unittest
import unittest.mock as mock
import asyncio


def return_author(*args, **kwargs):
    author_out = AuthorOut(id=1, name="test")
    return author_out


class TestAuthorRouter(unittest.TestCase):

    @mock.patch.object(AuthorService, 'save_author')
    def test_create_author_without_error(self, save_author_mock):
        save_author_mock.side_effect = return_author
        response = Response()
        author = AuthorIn(name="test")
        author_router = AuthorRouter()

        result = asyncio.run(author_router.create_author(author, response))

        self.assertEqual(result, AuthorOut(id=1, name="test", links=get_links(router)))
        save_author_mock.assert_called_once_with(author)
        self.assertEqual(response.status_code, 200)

    @mock.patch.object(AuthorService, 'save_author')
    def test_create_author_with_error(self, save_author_mock):
        save_author_mock.return_value = AuthorOut(name="test", errors={'errors': ['test']})
        response = Response()
        author = AuthorIn(name="test")
        author_router = AuthorRouter()

        result = asyncio.run(author_router.create_author(author, response))

        self.assertEqual(result, AuthorOut(name="test", errors={'errors': ['test']}, links=get_links(router)))
        save_author_mock.assert_called_once_with(author)
        self.assertEqual(response.status_code, 422)
