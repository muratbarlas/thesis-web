from dotenv import load_dotenv
from openai import OpenAI
import os
import csv
load_dotenv('.env')
api_key = os.getenv('api_key')
print(api_key)
# client = OpenAI(api_key= api_key_)
#
#
# with open('fox_gpt.csv', 'w', newline='') as file:
#   writer = csv.writer(file)
#   for i in range(50):
#     completion = client.chat.completions.create(
#       model=model_,
#       messages=[
#         {"role": "system", "content": "You are an assistant that generates news headlines"},
#         {"role": "user", "content": "Generate a news headline"}
#       ]
#     )
#     reply = completion.choices[0].message.content
#     writer.writerow([reply])
#     print(reply)