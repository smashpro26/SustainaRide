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


os.environ["REPLICATE_API_TOKEN"] = 'r8_8ixutGw694ewxrQeN4hA3DE1toTBRrr3H1VkQ'  


output = replicate.run(
    "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
    input={"prompt": ...}
)
# The meta/llama-2-70b-chat model can stream output as it's running.
# The predict method returns an iterator, and you can iterate over that output.
for item in output:
    # https://replicate.com/meta/llama-2-70b-chat/versions/02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3/api#output-schema
    print(item, end="")