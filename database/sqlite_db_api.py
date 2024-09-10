import os
import sqlite3

from database.sqlite_db_config import HISTORY_TABLE_NAME, FULL_DIRECTORY_WITH_DB_NAME
from sql_transpiler_logic.util.util_file_path import extract_directory, fs_create_directory

""" function api starts from here """


def db_ops(_func):
    """
    helps to init database operations on init. Must add this on every page
    a decorator, takes in a function and returns a function
    """

    def wrapper(*args, **kwargs):
        initialize_database(print_logs=False)
        return _func(*args, **kwargs)

    return wrapper


def initialize_database(db_name: str = FULL_DIRECTORY_WITH_DB_NAME, print_logs=False):
    """
    Initializes a SQLite database with the specified tables if the database does not exist.
    :param db_name: Name of the SQLite database file.
    """
    # Extract directory from db_name, if there's a directory component
    _extracted_dir = extract_directory(db_name)
    if _extracted_dir and not os.path.exists(_extracted_dir):
        fs_create_directory(_extracted_dir)

    if not os.path.exists(db_name):
        if print_logs: print(f"Database {db_name} not found. Initializing new database...")
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute(f"""
        CREATE TABLE {HISTORY_TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            base_query_type TEXT NOT NULL,
            base_query TEXT NOT NULL,
            transformed_query_type TEXT NOT NULL,
            transformed_query TEXT NOT NULL
        )
        """)

        conn.commit()
        conn.close()
        if print_logs: print(f"Database {db_name} initialized successfully.")
    else:
        if print_logs: print(f"Database {db_name} already exists. No action taken.")


def insert_record_into_transpiler_history(
        _record: list,
        _timestamp: str,
        _db_name: str = FULL_DIRECTORY_WITH_DB_NAME,
):
    """
    Inserts a record into the TRANSPILER_HISTORY table in the specified SQLite database.


    :param _record: A tuple containing the values to insert. Should be in the format:
                   (timestamp, base_query, base_query_type, transformed_query, transformed_query_type)
    :param _timestamp: basically the datetime now
    :param _db_name: Name of the SQLite database file.
    """
    try:
        conn = sqlite3.connect(_db_name)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO TRANSPILER_HISTORY (
            timestamp,
            base_query_type,
            base_query,
            transformed_query_type,
            transformed_query
        )
        VALUES (?, ?, ?, ?, ?)
        """, _record)

        conn.commit()
        conn.close()
        print(f"Record inserted successfully, Timestamp: {_timestamp}")
    except Exception as e:
        print(e)
        print("Unable to insert new record !")


if __name__ == "__main__":
    initialize_database(FULL_DIRECTORY_WITH_DB_NAME)