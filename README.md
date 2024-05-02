**Fut_ChatBot Version 2!**

how to run: 

run chatbot.py


Requirements:
- pandas
- openai
- sqlite3


Breakdown of the code:

Functions load_csvs_to_sqlite and query_data from database utils:

This functions are in charge of making a temporary sql database with the football datasets
that we have gather from kaggle. The query_data function is in charge of querying the database
and return the result.

Function run_chat from openai_query:
This funciton is the one that calls the open ai api and asks to make an sql query to answer the user data retrival request.
This function only returns an sql query that will then be run by the query_data function.

Function run_explanation from openai_explanation:
This function takes the data retrieve from the query_data function and ask to the open ai api to use the data and the previous
user's questions to generate a response.

This is a detailed Work Flow of how the chatbot creates the response for the user:

[Chatbot Work Flow](chatbot_workflow.pdf)


