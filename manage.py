#!/usr/bin/python3
import unittest
import sys

if 'test' in sys.argv:
    loader = unittest.TestLoader()

    try:
        tests_dir = f'tests/{sys.argv[2]}_tests'
    except IndexError:
        tests_dir = 'tests'
    tests = loader.discover(tests_dir)

    runner = unittest.TextTestRunner()
    success = runner.run(tests).wasSuccessful()

    exit(0 if success else 1)
