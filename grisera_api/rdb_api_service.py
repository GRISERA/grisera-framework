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
                password=rdb_api_password,
                port=rdb_api_port
            )
        except psycopg2.Error as e:
            print("Error connecting to the database:", e)

    def convert_to_dict(self, records, column_names):
        data_list = []
        for row in records:
            row_dict = dict(zip(column_names, row))
            data_list.append(row_dict)
        return data_list

    def get(self, table_name):
        cursor = self.connection.cursor()
        query = "SELECT * FROM " + table_name
        cursor.execute(query)
        result = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        data_list = self.convert_to_dict(result, column_names)
        cursor.close()
        return data_list

    def get_with_id(self, table_name, id):
        cursor = self.connection.cursor()
        query = "SELECT * FROM " + table_name + " WHERE id = " + str(id)
        cursor.execute(query)
        result = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        data_list = self.convert_to_dict(result, column_names)
        cursor.close()
        return data_list[0]
    
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

    def post(self, table_name, record):
        try:
            cursor = self.connection.cursor()
            
            columns = ', '.join(record.keys())
            placeholders = ', '.join(['%s'] * len(record))
            values = list(record.values())
            
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) RETURNING *"
            
            cursor.execute(query, values)
            row = cursor.fetchone()

            new_record = {}
            for desc, value in zip(cursor.description, row):
                new_record[desc.name] = value
            
            self.connection.commit()
            cursor.close()
            return new_record
        except psycopg2.Error as error:
            self.connection.rollback()
            return error



