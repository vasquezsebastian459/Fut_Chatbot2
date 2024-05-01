from database_utils import load_csvs_to_sqlite, query_data
from openai_query import run_chat, clean_query
from openai_explanation import run_explanation
import json
from datetime import datetime
from json_encoder import CustomJSONEncoder

def interactive_chatbot_session(connection, max_attempts=5):
    context = []
    print("I am your assistant for today. I can help you get any information you need about the Premier League 2021/2022 season.")
    for i in range(max_attempts):
        question = input("Ask a question (type 'exit' to quit): ")
        if question.lower() == 'exit':
            break

        output = {'Interaction': i, 'Question': question}
        
        # Get SQL query from chatbot
        completion = run_chat(question, context)
        query = completion.choices[0].message.content
        query = clean_query(query)
        output['SQL Query'] = query
        
        # Execute SQL query
        data = query_data(connection, query)
        output['SQL Data'] = data

        temp_context = context.copy()
        temp_context.append(output)
        completion = run_explanation(question, temp_context)
        response = completion.choices[0].message.content
        output['Generated Explanation'] = response
        print("Explanation:", response)
        context.append(output)

    # Save the conversation context to a JSON file named by the current timestamp
    timestamp = datetime.now().strftime("%m%d%H%M%S")
    json_filename = f"conversations/chat_session_{timestamp}.json"
    with open(json_filename, 'w') as f:
        json.dump(context, f, indent=4, cls=CustomJSONEncoder)
    
    print(f"Session saved to {json_filename}")
    connection.close()
    print('SQLite connection closed')

# Example usage
csv_paths = ['dataset/all_match_results.csv', 'dataset/all_players_stats.csv', 'dataset/points_table.csv']
table_names = ['match_result', 'player_stats', 'points_table']
connection = load_csvs_to_sqlite(csv_paths, table_names)
interactive_chatbot_session(connection)
