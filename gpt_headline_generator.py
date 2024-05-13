from dotenv import load_dotenv
from openai import OpenAI
import os
import csv
load_dotenv('.env')
api_key_ = os.getenv('api_key')
reddit_model = os.getenv('reddit_model')
fox_model =  os.getenv('fx_news_model')



client = OpenAI(api_key= api_key_)


with open('reddit_gpt.csv', 'w', newline='') as file:
  writer = csv.writer(file)
  for i in range(100):
    completion = client.chat.completions.create(
      model=reddit_model,
      messages=[
        {"role": "system", "content": "You are an assistant that generates news headlines"},
        {"role": "user", "content": "Generate a news headline"}
      ]
    )
    reply = completion.choices[0].message.content
    writer.writerow([reply])
    print(reply)