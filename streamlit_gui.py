import streamlit as st
from database_utils import load_csvs_to_sqlite, query_data
from openai_query import run_chat, clean_query
from openai_explanation import run_explanation
import json
from datetime import datetime
from json_encoder import CustomJSONEncoder

# Initialize the database connection
csv_paths = ['dataset/all_match_results.csv', 'dataset/all_players_stats.csv', 'dataset/points_table.csv']
table_names = ['match_result', 'player_stats', 'points_table']
connection = load_csvs_to_sqlite(csv_paths, table_names)

# Initialize the conversation context
if 'chat_context' not in st.session_state:
    st.session_state['chat_context'] = []

def chatbot_query(question):
    context = st.session_state['chat_context']
    output = {'Question': question}

    # Get SQL query from chatbot
    completion = run_chat(question, context)
    query = completion.choices[0].message.content
    query = clean_query(query)
    output['SQL Query'] = query

    # Execute SQL query
    data = query_data(connection, query)
    output['SQL Data'] = data

    # Add current interaction to context for more accurate future responses
    temp_context = context.copy()
    temp_context.append(output)

    completion = run_explanation(question, temp_context)
    response = completion.choices[0].message.content
    output['Generated Explanation'] = response

    # Update the session state with new context
    st.session_state['chat_context'].append(output)
    return json.dumps(response, indent=4, cls=CustomJSONEncoder)

def save_session():
    context = st.session_state['chat_context']
    timestamp = datetime.now().strftime("%m%d%H%M%S")
    json_filename = f"conversations/chat_session_{timestamp}.json"
    with open(json_filename, 'w') as f:
        json.dump(context, f, indent=4, cls=CustomJSONEncoder)
    return f"Session saved to {json_filename}"

def main_page():
    st.title("Premier League 2021/2022 AI Chatbot ⚽")
    st.write("Ask any question about the Premier League 2021/2022 season and get explanations based on actual data. 📊")

    question = st.text_input("Enter your question:", value="")
    if st.button("Send", key='send'):
        response = chatbot_query(question)
        st.text_area("Response:", value=response, height=300)

    if st.button("Save Session", key='save', on_click=save_session):
        st.sidebar.write("Session data saved successfully.")

def login_page():
    st.session_state['logged_in'] = False
    st.title("Login to Premier League 2021/2022 AI Chatbot 🚪")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if username and password:  # Add your authentication logic here
            st.session_state['logged_in'] = True
            st.experimental_rerun()

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    main_page()
else:
    login_page()
