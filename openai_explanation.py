from openai import OpenAI

def run_explanation(question,prev_conv,temperature = 0.2):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content":
                f"""
                Your task is to take the context information and generate a short explanation for the user.
                First see the sql Data generated in the last interaction, if it is relevant to the user question then answer the question
                using that data only.
                If the last interaction is not relevant then look for the other interactions.
                If nothing is relevant from the other interactin then ask the user to clarify the question.
                Generate an explanation only based on the context and Data provided. 
                
                Previous Conversation:
                {prev_conv}

                """
             },
            {"role": "user", "content": question
             
             }
        ],
        temperature=temperature 
    )
    return completion