
from openai import OpenAI

def run_chat(question,context, temperature=0.4):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content":
                f"""
                You are a Premier League chatbot that is made answer questions about the Premier League. If the user asks a question
                you must create an sql query to retrieve the information. Only output the sql query. Nothing else.

                This is the schema of the database:

                Table: match_result: these are the results of the matches in the Premier League
                columns: Date,HomeTeam,Result,AwayTeam

                Table: player_stats: these are individual player stats
                columns: Team,JerseyNo,Player,Position,Apearances,Substitutions,Goals,Penalties,YellowCards,RedCards
                
                Table: points_table: these are the current standings of the teams in the Premier League
                columns: Pos,Team,Pld,W,D,L,GF,GA,GD,Pts

                Make sure that the sql query is valid and can be run on the database.
                Make sure the corresponding colums you used are in the expected table.
                Make sure the query starts with SELECt and ends with a semicolon ';'

                Context for the question:
                {context}
                
                """
             },
            {"role": "user", "content": question
             
             }
        ],
        temperature=temperature 
    )
    return completion


def clean_query(query):
    query = query.replace('\n', ' ')
    # Find the position of the start and end of the query
    start_pos = query.find("SELECT")
    end_pos = query.rfind(";")
    query = query[start_pos:end_pos+1] if start_pos != -1 and end_pos != -1 else "Query not found"


    # query = query.replace(';', '')
    # query = query.strip()
    return query

