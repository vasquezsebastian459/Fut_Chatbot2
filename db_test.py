import pandas as pd
import sqlite3
from openai_query import run_chat, clean_query
from openai_explanation import run_explanation

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


# Example usage
csv_paths = ['dataset/all_match_results.csv', 'dataset/all_players_stats.csv', 'dataset/points_table.csv']
table_names = ['match_result', 'player_stats', 'points_table']
connection = load_csvs_to_sqlite(csv_paths, table_names)


def run_sql_query(sql_query):
    result = query_data(connection, sql_query)
    return result 

query = "SELECT Team, Player FROM player_stats where Player = 'Bukayo Saka'"
result =run_sql_query(query)
print(result)