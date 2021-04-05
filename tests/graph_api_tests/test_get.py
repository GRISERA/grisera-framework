import graph_api.main as main
import unittest
import asyncio


class TestGet(unittest.TestCase):

    def test_root(self):
        expect = {"title": "Graph DB API"}
        expect.update({'links': main.get_links(main.app)})
        
        self.assertEqual(asyncio.run(main.root()), expect)
