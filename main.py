import os
import requests
from openai import OpenAI
import anthropic
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from IPython import display 
import markdown
# import google.generativeai
from typing import List
import gradio as gr 
import json 

#load environment variables 
load_dotenv()

# message = "Hello, GPT! This is my first call to you"
# response = openai.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":message}])
# print(response.choices[0].message.content)

# Functions

def messages_for(system_prompt, user_prompt):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
        ] 
#LLM Tools. Functions that can be used my LLMs to utilize tools.

def build_tool_schema(name: str, description: str, properties: dict, required: list) -> dict:
    """
    Builds a tool schema for a Claude-compatible tool.

    Args:
        name (str): Name of the tool.
        description (str): Description of what the tool does.
        properties (dict): Dictionary of input fields and their definitions.
        required (list): List of required field names.

    Returns:
        dict: Tool schema dictionary.
    """
    return {
        "name": name,
        "description": description,
        "input_schema": {
            "type": "object",
            "properties": properties,
            "required": required
        }
    }
    
    




# Classes 

class Website:
    
    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        
        self.url = url
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)
        
        
class LLM_Clients_OpenAI:
    """
    Creates LLM System Prompts for a LLM use cases    
    """
    
    def __init__(self, model="gpt-4o-mini"):        
                    
        self.system_prompt = ""                
        self.user_prompt = ""
        
            
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.openai = OpenAI()    
        self.MODEL =  model  
  
    #LLM actions 
    
    def summarize(self, message):   
        response = self.openai.chat.completions.create(
        model = self.MODEL,
        messages = message
        )
        return response.choices[0].message.content
    
    def steam_summarize(self, message):
        stream_response = self.openai.chat.completions.create(
            model = self.MODEL,
            messages = message,
            stream = True
        )
        
        response = ""
        display_handle = display(Markdown(""), display_id=True)
        for chunk in stream:
            response += chunk.choices[0].delta.content or ''
            response = response.replace("```","").replace("markdown", "")
            update_display(Markdown(response), display_id=display_handle.display_id)
    
    #LLM Client Types    
    def website(self, website):
        
        website = Website(website)
        self.system_prompt = "You are an assistant that analyzes the contents of a website and provides a short summary, ignoring text that might be navigation related. Respond in markdown."
        
        self.user_prompt = f"You are looking at a website titled {website.title}. The contents of this website is as follows; please provide a short summary of this website in markdown. If it includes news or announcements, then summarize these too.\n\n {website.text}"
        
        return(self.summarize(messages_for(self.system_prompt, self.user_prompt)))
    
    def tech_assistant(self, tech_question):
        
        self.system_prompt = "You are a technical expert in AI and software development. You will be teaching and explaning technical questions to an high school student."
        
        self.user_prompt = tech_question
        
        return (self.summarize(messages_for(self.system_prompt, self.user_prompt)))
    
class LLM_Clients_Claude:
    def __init__(self, model='claude-3-7-sonnet-latest', temperature=1, tokens=200):
        self.system_prompt = ''
        self.user_prompt = ''
        
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.claude = anthropic.Anthropic()
        self.MODEL = model
        self.TEMPERATURE = temperature
        self.TOKENS = tokens
        self.conversation_history = []
    
    # def create_prompt(self, system_prompt, user_prompt):
    #     self.system_prompt = system_prompt
    #     self.user_prompt = user_prompt        
    #     return  {"role": "user", "content": user_prompt}
                
    def chat(self, message, history):
        
        # Convert chat history to Claude-style messages
        print(history)
        messages = []
        for turn in history:
            messages.append({"role": turn["role"], "content": turn["content"]})
        messages.append({"role": "user", "content": message})

        # Stream response from Claude
        stream = self.claude.messages.create(
            model=self.MODEL,
            max_tokens=self.TOKENS,
            temperature=self.TEMPERATURE,
            messages=messages,
            stream=True
         )

        full_response = ""
        for chunk in stream:
            if chunk.type == "content_block_delta" and hasattr(chunk.delta, "text"):
                text = chunk.delta.text
                full_response += text
                yield full_response  # Stream to Gradio
        
        
        
        
                
       
            

                    
        

if __name__ == "__main__":
    ai = LLM_Clients_Claude() 
    
    # while True:
    #     user_input = input("Question: ")               
    #     if user_input.lower() == "exit":
    #         break
    #     else:
    #         response  = ai.chat(user_input)
    #         for sentence in response:
    #             print(sentence)
                
            
    
    gr.ChatInterface(fn=ai.chat, type="messages").launch()