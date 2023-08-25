import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
result = openai.Image.create(prompt="airplain flying in the sea", 
                             n=5, 
                             size="256x256", 
                             user="sanaigon")

print(result)
