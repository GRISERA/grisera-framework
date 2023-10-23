import psycopg2
from rdb_api_config import *


class RdbApiService:
    """
    Object that handles direct communication with mongodb
    """

    MONGO_ID_FIELD = "_id"
    MODEL_ID_FIELD = "id"

    def __init__(self):
        """
        Initialize and establish a connection to the database.
        """
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
        """
        Convert rows fetched from the database into a list of dictionaries.

        :param records: Rows fetched from the database.
        :param column_names: Names of the columns.
        :return: List of dictionaries representing the rows.
        """
        data_list = []
        for row in records:
            row_dict = dict(zip(column_names, row))
            data_list.append(row_dict)
        return data_list

    def get(self, table_name):
        """
        Fetch all records from a table.

        :param table_name: Name of the table.
        :return: List of dictionaries representing rows from the table.
        """
        cursor = self.connection.cursor()
        query = "SELECT * FROM " + table_name
        cursor.execute(query)
        result = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        data_list = self.convert_to_dict(result, column_names)
        cursor.close()
        return data_list

    def get_with_id(self, table_name, id):
        """
        Fetch a record from a table using its ID.

        :param table_name: Name of the table.
        :param id: ID of the record to fetch.
        :return: Dictionary representing the row or None if not found.
        """
        cursor = self.connection.cursor()
        query = "SELECT * FROM " + table_name + " WHERE id = " + str(id)
        cursor.execute(query)
        result = cursor.fetchall()
        if not result:
            return None
        column_names = [desc[0] for desc in cursor.description]
        data_list = self.convert_to_dict(result, column_names)
        cursor.close()
        return data_list[0]

    def post(self, table_name, record):
        """
        Insert a record into a table.

        :param table_name: Name of the table.
        :param record: Dictionary containing column names and values.
        :return: Inserted record as a dictionary or error.
        """
        try:
            cursor = self.connection.cursor()
            
            columns = ', '.join(record.keys())
            placeholders = ', '.join(['%s'] * len(record))
            values = list(record.values())
            
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) RETURNING *"
            
            cursor.execute(query, values)
            row = cursor.fetchone()

            data_list = {}
            for desc, value in zip(cursor.description, row):
                data_list[desc.name] = value

            self.connection.commit()
            cursor.close()
            return data_list
        except psycopg2.Error as error:
            self.connection.rollback()
            return error
        
    def put(self, table_name, id, updated_record):
        """
        Update a record in a table by its id.

        :param table_name: Name of the table
        :param id: ID of the record to update
        :param updated_record: Dictionary containing columns and their new values
        :return: Updated record or error
        """
        try:
            cursor = self.connection.cursor()

            set_statements = ', '.join([f"{column} = %s" for column in updated_record.keys()])
            values = list(updated_record.values())
            values.append(id)
            
            query = f"UPDATE {table_name} SET {set_statements} WHERE id = %s RETURNING *"
            
            cursor.execute(query, values)
            row = cursor.fetchone()

            data_list = {}
            for desc, value in zip(cursor.description, row):
                data_list[desc.name] = value

            self.connection.commit()
            cursor.close()
            return data_list
        except psycopg2.Error as error:
            self.connection.rollback()
            return error

        
    def delete_with_id(self, table_name, id):
        """
        Delete a record from a table using its ID.

        :param table_name: Name of the table.
        :param id: ID of the record to delete.
        """
        cursor = self.connection.cursor()
        query = "DELETE FROM " + table_name + " WHERE id = %s"
        cursor.execute(query, (id,))
        self.connection.commit()
        cursor.close()