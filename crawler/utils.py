import pandas as pd
import sqlite3


def get_connection(database_address):
    return sqlite3.connect(database_address)


def get_table(table_name, database_address):
    connection = get_connection(database_address)
    return pd.read_sql_query(f"SELECT * FROM {table_name}", connection)
