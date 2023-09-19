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
preprompt = "You are a helpful assistant who provides information about travelling from place to place.You should provide prices for the public transportation methods you suggest. You do not respond as 'User' or pretend to be 'User'. You only respons once as 'Assistant"

def get_answer(prompt):

    output = replicate.run("meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3", 
                        input={'prompt': f"{preprompt} {prompt} Assistant: "},
                        max_length = 128
                        )

    fullresponse = ''
    for item in output:
        fullresponse += item
    print(fullresponse)
    return fullresponse



