# parameters of graph_api used in API
import os

graph_api_host = os.environ.get('GRAPH_API_HOST') or 'localhost'
graph_api_port = 8000
graph_api_address = "http://{}:{}".format(graph_api_host, graph_api_port)
