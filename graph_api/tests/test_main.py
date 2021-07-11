import main
import unittest
import asyncio


class MainTestCase(unittest.TestCase):

    def test_root(self):
        expect = {"title": "Graph DB API",
                  "links": main.get_links(main.app)}

        result = asyncio.run(main.root())
        
        self.assertEqual(result, expect)
