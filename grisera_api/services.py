import os
from enum import Enum

from activity.activity_service import ActivityService
from activity.activity_service_graphdb import ActivityServiceGraphDB


class PersistenceTypes(Enum):
    GRAPHDB = 1
    ONTOLOGY = 2


class Services:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Services, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.persistence_type = os.environ.get('PERSISTENCE_TYPE') or PersistenceTypes.GRAPHDB

    def activity_service(self) -> ActivityService:
        if self.persistence_type == PersistenceTypes.GRAPHDB:
            return ActivityServiceGraphDB()
        else:
            return ActivityService
