import pandas as pd
import sqlite3
from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPICallError, RetryError
from google.cloud.bigquery import LoadJobConfig, SchemaUpdateOption
import os
import datetime
import time
import numpy as np


from tqdm import tqdm

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + "/google.json"

sqlite_db_path = [    
                   '../measurement_data/path.db' ,
                  ]

dataset_name = 'dataset'

tables = ['callstacks', 'cookies',
          'event_listeners',
          'removed_event_listeners', 'requests', 'responses', 'interactions']

 

def read_from_sqlite_in_chunks(connection, table_name, chunksize=60000):
    query = f"SELECT * FROM {table_name}"
    for chunk in pd.read_sql_query(query, connection, chunksize=chunksize):
        yield chunk

def load_chunk_to_bigquery(chunk_df, table_id, client, job_config, file):
    try:
        job = client.load_table_from_dataframe(chunk_df, table_id, job_config=job_config)
        job.result()
        print(f"✅ Chunk loaded to {table_id} at {datetime.datetime.now()} from file: {os.path.basename(file)}")
        return True
    except Exception as e:
        print(f"❌ Failed to load chunk to {table_id} with error: {e}")
        print(f"File: {file}")
        return False


# Initialize a BigQuery client
client = bigquery.Client()


for file in sqlite_db_path:

    # check if file exists
    if not os.path.exists(file):
        print(f"File {file} does not exist. Skipping...")
        continue

    conn = sqlite3.connect(file)
    file_failed = False
    break_outer = False
    for table in tables:
        if break_outer:
            print(f"\033[1;33;41m ⚠️ Skipping rest of file {file} due to earlier failure \033[0m")
            continue
        if table == 'callstacks':
            table_bq = 'callstacks' + str(np.random.randint(1, 21))
        elif table == 'event_listeners':
            table_bq = 'event_listeners' + str(np.random.randint(1, 21))
        else:
            table_bq = table
            

        job_config = LoadJobConfig(schema_update_options=[
            SchemaUpdateOption.ALLOW_FIELD_ADDITION])
        table_id = f"{client.project}.{dataset_name}.{table_bq}"

        for chunk in read_from_sqlite_in_chunks(conn, table):
            if chunk.empty:
                print(f"Skipping table {table} as it contains no rows.")
                continue
            chunk['measurement'] = os.path.basename(file)
            # Ensure column data types are correct
            for col in chunk.columns:
                if col in ['site_id']:  # Specify other columns as needed
                    chunk[col] = chunk[col].astype(str)
                elif col == 'is_set':
                    chunk[col] = chunk[col].astype(str)
                elif col == 'init_stack':
                    # Assuming 'init_stack' should be a string, handle any special cases:
                    chunk[col] = chunk[col].astype(str)
                elif col == 'start_time':
                    # Convert start_time column to datetime
                    chunk[col] = pd.to_datetime(chunk[col], errors='coerce')
                elif col == 'end_time':
                    # Convert start_time column to datetime
                    chunk[col] = pd.to_datetime(chunk[col], errors='coerce')

            original_table_bq = table_bq  # Remember original table name

            for attempt in range(5):
                success = load_chunk_to_bigquery(chunk, table_id, client, job_config, file)
                if success:
                    break
                else:
                    print(f"\033[1;37;41m ❌ Retrying to load chunk to {table_id} (Attempt {attempt + 1}/5) \033[0m") 
                    time.sleep(15)

                    # Change table name for specific high-volume tables
                    if table == 'callstacks':
                        table_bq = 'callstacks' + str(np.random.randint(1, 21))   
                    elif table == 'event_listeners':
                        table_bq = 'event_listeners' + str(np.random.randint(1, 21))   
                    else:
                        table_bq = original_table_bq  

                    table_id = f"{client.project}.{dataset_name}.{table_bq}"

                    if attempt == 4:
                        print(f"🚨 Failed to load chunk to {original_table_bq} or fallback tables after 5 attempts. Moving on.")

                        # Move file to failed_ prefix
                        failed_file = os.path.join(
                            os.path.dirname(file),
                            "failed_" + os.path.basename(file)
                        )
                        conn.close()  # ensure SQLite file is released
                        os.rename(file, failed_file)

                        print(f"\033[1;37;41m ❌ Moved failed file to {failed_file} \033[0m")
                        file_failed = True  # mark file as failed
                        break  # break retry loop 
            if file_failed:
                break_outer = True
                break
    # Close the SQLite connection
    try:
        conn.close() 
    except sqlite3.Error as e:
        print(f"❌ Error closing SQLite connection: {e}") 

    # After closing the connection, rename the SQLite file by appending "_done"
    if not file_failed:
        # Rename to mark as done
        new_file_name = file.replace("25k", "done_25k")
        os.rename(file, new_file_name)

        print("\033[1;30;42m ✅ Renamed {} to {} \033[0m".format(file, new_file_name))
        print("🕒 Time: " + str(datetime.datetime.now()))
        print("Sleeping for 15 seconds before processing the next file...")
        time.sleep(15)
