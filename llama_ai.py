import customtkinter
from bardapi import Bard
import os
import replicate

#token = os.environ.get('BARD_API_KEY')
#token = "bAhvyXbVfYgo1P4OjLbsuHh1xfi62NOfWEzSNKy0ueB9JGzF1jJMAykpHGMDvqHFTXRbIA."
#bard = Bard(token=token)
'''
def bard_GetAnswer(prompt):
    answer = bard.get_answer(prompt)
    return answer'''


#os.environ["REPLICATE_API_TOKEN"]  = 'r8_8ixutGw694ewxrQeN4hA3DE1toTBRrr3H1VkQ' 
preprompt = "You are a helpful assistant who provides information about travelling from place to place.You should provide prices for the public transportation methods you suggest. Seperate each mode of transport that you give clearly. You do not respond as 'User' or pretend to be 'User'. You only respons once as 'Assistant"

def get_answer(prompt):

    output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', # LLM model
                        input={"prompt": f"{preprompt} {prompt} Assistant: ", # Prompts
                        "temperature":0.1, "top_p":0.9, "max_length":512})  # Model parameters
     

    fullresponse = ''
    for item in output:
        fullresponse += item
    print(fullresponse)
    return fullresponse




