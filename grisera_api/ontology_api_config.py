# parameters of graph_api used in API
import os

ontology_api_host = os.environ.get('ONTOLOGY_API_HOST') or 'localhost'
ontology_api_port = os.environ.get('ONTOLOGY_API_PORT') or '8000'
ontology_api_address = "http://{}:{}".format(ontology_api_host, ontology_api_port)
