import pandas as pd
import sqlite3

def load_csvs_to_sqlite(csv_file_paths, table_names):
    # Connect to a SQLite memory database
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    
    # Load each CSV file into a separate table
    for csv_file, table_name in zip(csv_file_paths, table_names):
        df = pd.read_csv(csv_file)
        df.to_sql(table_name, conn, index=False, if_exists='replace')
    
    return conn

def query_data(conn, sql_query):
    # Execute SQL query
    df_query_result = pd.read_sql_query(sql_query, conn)
    return df_query_result