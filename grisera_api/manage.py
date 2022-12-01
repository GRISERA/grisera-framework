#!/usr/bin/python3
import unittest
import sys

if 'test' in sys.argv:
    loader = unittest.TestLoader()
    tests_dir = 'tests'
    test_dir_GraphDB = '/tests_graphdb'
    tests = loader.discover(tests_dir + test_dir_GraphDB)

    runner = unittest.TextTestRunner()
    success = runner.run(tests).wasSuccessful()

    exit(0 if success else 1)
