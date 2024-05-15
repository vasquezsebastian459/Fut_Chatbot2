import streamlit as st
from auth import authenticate_user, register_user
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

# Function to display chat messages
def display_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Function for generating LLM response
def generate_response(question, connection):
    # Use the existing context from session state
    context = st.session_state.context.copy()
    output = {}

    # Get SQL query from chatbot
    # Simulating the question since this is a test
    query = "SELECT Player, Goals FROM player_stats ORDER BY Goals DESC LIMIT 1;"
    query = clean_query(query)
    output['SQL Query'] = query
    
    # Execute SQL query
    data = query_data(connection, query)
    output['SQL Data'] = data

    # Update context with the new output
    context.append(output)
    
    # Simulate explanation response
    response = "KLK MAMAGUEBO"
    output['Generated Explanation'] = response
    
    # Update the context in session state
    st.session_state.context = context
    
    return response

# Example usage
csv_paths = ['dataset/all_match_results.csv', 'dataset/all_players_stats.csv', 'dataset/points_table.csv']
table_names = ['match_result', 'player_stats', 'points_table']
connection = load_csvs_to_sqlite(csv_paths, table_names)

# Manage navigation state
if "page" not in st.session_state:
    st.session_state.page = "login"

# Handle navigation between pages
def show_login_page():
    st.session_state.page = "login"
    st.experimental_rerun()

def show_register_page():
    st.session_state.page = "register"
    st.experimental_rerun()

# User login
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    if st.session_state.page == "login":
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            authenticated, message = authenticate_user(username, password)
            if authenticated:
                st.session_state.authenticated = True
                st.experimental_rerun()
            else:
                st.error(message)

        if st.button("Go to Register Page"):
            show_register_page()
    elif st.session_state.page == "register":
        st.header("Register")
        reg_username = st.text_input("Register Username")
        reg_password = st.text_input("Register Password", type="password")
        if st.button("Register"):
            registered, message = register_user(reg_username, reg_password)
            if registered:
                st.success(message)
                show_login_page()
            else:
                st.error(message)
        
        if st.button("Back to Login"):
            show_login_page()
else:
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
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
