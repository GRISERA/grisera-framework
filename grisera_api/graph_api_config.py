# parameters of graph_api used in API
import os

graph_api_host = os.environ.get('GRAPH_API_HOST') or 'localhost'
graph_api_port = os.environ.get('GRAPH_API_PORT') or '8000'
graph_api_address = "http://{}:{}".format(graph_api_host, graph_api_port)
graph_api_controller_class_type = os.environ.get('graph_api_controller_class_type') or 'default'
