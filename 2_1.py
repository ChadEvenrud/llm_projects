import os
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai
import anthropic


load_dotenv()

openai = OpenAI()
claude = anthropic.Anthropic()
google.generativeai.configure()


system_message = 'You are a Water Polo coach assistant that helps the coach develop offensive plays'
user_prompt = 'Develop a water polo play for six on 5'

prompt = [
    {'role': 'system', 'content': system_message},
    {'role': 'user', 'content': user_prompt}
]

# completion = openai.chat.completions.create(model='gpt-3.5-turbo', messages=prompt)
# print(completion.choices[0].message.content)


messages = claude.messages.stream(
    model = "claude-3-5-sonnet-20241022",
    max_tokens=200,
    temperature=0.7,
    system=system_message,
    messages=[{
        'role':'user','content': user_prompt
    }]
    
)

with messages as stream:
    for text in stream.text_stream:
        print(text, end='', flush=True)
        

    