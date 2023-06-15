import os

rdb_api_host = os.environ.get("RDB_HOST") or "localhost"
rdb_api_port = os.environ.get("RDB_PORT") or "8000"
rdb_api_address = f"http://{rdb_api_host}:{rdb_api_port}"
