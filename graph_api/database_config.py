# parameters of graph database used in API
import os

db_host = os.environ.get('DB_HOST') or 'localhost'

database = {
    "address": "http://{}:7474".format(db_host),
    "name": "neo4j",
    "commit_path": "/db/{database_name}/tx/commit",
    "user": "neo4j",
    "passwd": "grisera",
}
