import streamlit as st
import random

from database_utils import load_csvs_to_sqlite, query_data
from openai_query import run_chat, clean_query
from openai_explanation import run_explanation

# App title and page configuration
st.set_page_config(page_title="Driblab Chatbot")

# Custom CSS for styling
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #0044cc;
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #f1f1f1;
        color: #000;
    }
    .stButton > button {
        background-color: #0044cc;
        color: white;
    }
    .st-chat-message {
        background-color: #e6f2ff;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .st-chat-message.user {
        color: #0044cc;
        font-weight: bold;
    }
    .st-chat-message.assistant {
        color: #0066ff;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar information
with st.sidebar:
    st.title('Premier League 21/22 Chatbot')
    st.markdown('Welcome to the Premier League Chatbot! Ask me anything about the Premier League 21/22.')

# Store LLM generated responses and conversation context
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]
if "context" not in st.session_state:
    st.session_state.context = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLM response
def generate_response(question, connection):
    # Use the existing context from session state
    context = st.session_state.context.copy()
    output = {}

    # Get SQL query from chatbot
    completion = run_chat(question, context)
    query = completion.choices[0].message.content
    query = clean_query(query)
    output['SQL Query'] = query
    
    # Execute SQL query
    data = query_data(connection, query)
    output['SQL Data'] = data

    # Update context with the new output
    context.append(output)
    
    # Get the explanation from the chatbot given the updated context
    completion = run_explanation(question, context)
    response = completion.choices[0].message.content
    output['Generated Explanation'] = response
    
    # Update the context in session state
    st.session_state.context = context
    
    return response

# Example usage
csv_paths = ['dataset/all_match_results.csv', 'dataset/all_players_stats.csv', 'dataset/points_table.csv']
table_names = ['match_result', 'player_stats', 'points_table']
connection = load_csvs_to_sqlite(csv_paths, table_names)

# User-provided prompt
if prompt := st.chat_input(disabled=False):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt, connection)
                st.write(response)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
