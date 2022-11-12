import asyncio
import unittest

import main


class MainTestCase(unittest.TestCase):

    def test_root(self):
        expect = {"title": "Ontology API",
                  "links": main.get_links(main.app)}

        result = asyncio.run(main.root())
        
        self.assertEqual(result, expect)
