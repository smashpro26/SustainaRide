import customtkinter
from bardapi import Bard
import os

#token = os.environ.get('BARD_API_KEY')

token = "bAhvyXbVfYgo1P4OjLbsuHh1xfi62NOfWEzSNKy0ueB9JGzF1jJMAykpHGMDvqHFTXRbIA."
bard = Bard(token=token)



def bard_GetAnswer(prompt):
    answer = bard.get_answer(prompt)
    return answer
    

