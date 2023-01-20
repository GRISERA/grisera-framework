# parameters of graph database used in API
import os

db_host = os.environ.get('DB_HOST') or 'localhost'
db_port = os.environ.get('DB_PORT') or '7474'

database = {
    "address": "http://{}:{}".format(db_host, db_port),
    "name": "neo4j",
    "commit_path": "/db/{database_name}/tx/commit",
    "user": "neo4j",
    "passwd": "griseragrisera",
}
