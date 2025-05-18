import os
import requests
from openai import OpenAI
from bs4 import BeautifulSoup
from dotenv import load_dotenv

#load environment variables 
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

openai = OpenAI()

# message = "Hello, GPT! This is my first call to you"
# response = openai.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":message}])
# print(response.choices[0].message.content)

headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}



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
        
class Prompts:
    """
    Creates LLM System Prompts and User Prompts       
    """
    
    def __init__(self):
    
        self.default_system = "You are an assistant that analyzes the contents of a website and provides a short summary, ignoring text that might be navigation related. Respond in markdown."   
    
    def user_prompt(self, message, website):
        self.default_user_message =         
        

if __name__ == "__main__":
    new_site = Website("https://cnn.com")
    
    llm_prompts = Prompts()
    print(llm_prompts.default_system)
    