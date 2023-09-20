import customtkinter
import os
import replicate

#A preprompt so that the ai knows how to act in response to a prompt
preprompt = "You are a helpful assistant who provides information about travelling from place to place.You should provide prices for the public transportation methods you suggest. Seperate each mode of transport that you give clearly. You do not respond as 'User' or pretend to be 'User'. You only respons once as 'Assistant"

#A function getting the answer from the ai
def get_answer(prompt):

    output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', # LLM model
                        input={"prompt": f"{preprompt} {prompt} Assistant: ", # Prompts
                        "temperature":0.1, "top_p":0.9, "max_length":512})  # Model parameters
     

    fullresponse = ''
    for item in output:
        fullresponse += item
    print(fullresponse)
    return fullresponse




