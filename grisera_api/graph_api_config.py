# parameters of graph_api used in API
import os

graph_api_host = os.environ.get('GRAPH_API_HOST') or 'localhost'

graph_api_address = "http://{}:18080".format(graph_api_host)
