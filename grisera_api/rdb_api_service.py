from enum import Enum
import psycopg2
from rdb_api_config import *


class Collections(str, Enum):
    ACTIVITY = "activity"
    ACTIVITY_EXECUTION = "activity_execution"
    APPEARANCE = "appearance"
    ARRANGEMENT = "arrangement"
    CHANNEL = "channel"
    EXPERIMENT = "experiment"
    LIFE_ACTIVITY = "life_activity"
    MEASURE = "measure"
    MEASURE_NAME = "measure_name"
    MODALITY = "modality"
    OBSERVABLE_INFORMATION = "observable_information"
    OBSERVABLE_INFORMATION_TIMESERIES = "observable_information_timeseries"
    PARTICIPANT = "participant"
    PARTICIPANT_STATE = "participant_state"
    PARTICIPANT_STATE_APPEARANCE = "participant_state_appearance"
    PARTICIPANT_STATE_PERSONALITY = "participant_state_personality"
    PARTICIPATION = "participation"
    PERSONALITY = "personality"
    RECORDING = "recording"
    REGISTERED_CHANNEL = "registered_channel"
    REGISTERED_DATA = "registered_data"
    SCENARIO = "scenario"
    TIMESERIES = "timeseries"
    TIMESERIES_METADATA = "timeseries_metadata"

class RdbApiService:
    
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
            cursor.close()
            return None
        column_names = [desc[0] for desc in cursor.description]
        data_list = self.convert_to_dict(result, column_names)
        cursor.close()
        return data_list[0]
    
    def get_records_with_foreign_id(self, table_name, column_name, id):
        cursor = self.connection.cursor()
<<<<<<< HEAD
        query = f"SELECT * FROM {table_name} WHERE {column_name} = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        records = [dict(zip(column_names, row)) for row in result]
        
        return records
=======
        query = "SELECT * FROM " + table_name + " WHERE " + column_name + "= %s"
        try:
            cursor.execute(query, (id,))
            result = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            records = [dict(zip(column_names, row)) for row in result]
            return {"records": records, "errors": None}
        except psycopg2.Error as error:
            return {"records":None, "errors": error.pgerror}
>>>>>>> rdb-stage

    def post(self, table_name, record):
        """
        Insert a record into a table.
<<<<<<< HEAD

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
            if row is None:
                cursor.close()
                return None

            data_list = {}
            for desc, value in zip(cursor.description, row):
                data_list[desc.name] = value

            self.connection.commit()
            cursor.close()
            return data_list
        except psycopg2.Error as error:
            self.connection.rollback()
            return error

=======

        :param table_name: Name of the table.
        :param record: Dictionary containing column names and values.
        :return: Inserted record as a dictionary or error.
        """
        try:
            cursor = self.connection.cursor()
            
            columns = ', '.join(record.keys())
            placeholders = ', '.join(['%s'] * len(record))
            values = list(record.values())
            
            query = "INSERT INTO " + table_name + "(" + columns + ") VALUES (" + placeholders + ") RETURNING *"
            
            cursor.execute(query, values)
            row = cursor.fetchone()

            data_list = {}
            for desc, value in zip(cursor.description, row):
                data_list[desc.name] = value

            self.connection.commit()
            cursor.close()
            return {"records": data_list, "errors": None}
        except psycopg2.Error as error:
            self.connection.rollback()
            return {"records": None, "errors": error.pgerror}
        
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
            
            query = "UPDATE "+ table_name + " SET " + set_statements + " WHERE id = %s RETURNING *"
            
            cursor.execute(query, values)
            row = cursor.fetchone()
            if row is None:
                cursor.close()
                return None

            data_dict = {}
            for desc, value in zip(cursor.description, row):
                data_dict[desc.name] = value

            self.connection.commit()
            cursor.close()
            return {"records":data_dict, "errors": None}
        except psycopg2.Error as error:
            self.connection.rollback()
            return {"records": None, "errors": error.pgerror}

>>>>>>> rdb-stage
        
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