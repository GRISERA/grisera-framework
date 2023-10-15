import os

rdb_api_host = os.environ.get("RDB_HOST") or "localhost"
rdb_api_port = os.environ.get("RDB_PORT") or "8000"
rdb_api_database_name = os.environt.get("RDB_NAME") or "db"
rdb_api_user = os.environt.get("RDB_USER") or "user"
rdb_api_password = os.environt.get("RDB_PASSWORD") or "123"
rdb_api_address = f"http://{rdb_api_host}:{rdb_api_port}"
