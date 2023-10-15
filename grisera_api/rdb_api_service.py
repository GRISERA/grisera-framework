import psycopg2
from rdb_api_config import *


class RdbApiService:
    """
    Object that handles direct communication with mongodb
    """

    MONGO_ID_FIELD = "_id"
    MODEL_ID_FIELD = "id"

    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host=rdb_api_host,
                database=rdb_api_database_name,
                user=rdb_api_user,
                password=rdb_api_password
            )
        except psycopg2.Error as e:
            print("Error connecting to the database:", e)

    def get(self, table_name):
        cursor = self.connection.cursor()
        query = "SELECT * FROM " + table_name
        cursor.execute(query)
        result = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        data_list = []
        for row in result:
            row_dict = dict(zip(column_names, row))
            data_list.append(row_dict)
        cursor.close()
        return data_list

    def get_with_id(self, table_name, id):
        cursor = self.connection.cursor()
        query = "SELECT * FROM " + table_name + "WHERE id == " + id
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def post(self, table_name, record):
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO " + table_name + " VALUES " + record
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
            return True
        except psycopg2.Error as error:
            self.connection.rollback()
            return error

    def put(self, table_name, id, column_values):
        try:
            cursor = self.connection.cursor()
            set_clause = ", ".join([f"{key} = %s" for key in column_values.keys()])
            update_query = f"UPDATE {table_name} SET {set_clause} WHERE id = %s;"
            cursor.execute(update_query, list(column_values.values()) + [id])
            self.connection.commit()
            cursor.close()
            return True
        except psycopg2.Error as error:
            self.connection.rollback()
            return error
