import os
from unittest import TestCase

from services.services import PersistenceTypes


class MongoTestCase(TestCase):
    def setUp(self):
        os.environ["PERSISTENCE_TYPE"] = str(PersistenceTypes.MONGODB.value)
