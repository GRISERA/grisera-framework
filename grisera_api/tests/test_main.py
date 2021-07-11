import main
import unittest
import asyncio


class TestMain(unittest.TestCase):

    def test_root(self):
        expect = {"title": "GRISERA API"}
        expect.update({'links': main.get_links(main.app)})

        self.assertEqual(asyncio.run(main.root()), expect)
