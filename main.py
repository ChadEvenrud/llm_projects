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



class Website:
    
    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        headers = {"User-Agent""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)
        


if __name__ == "__main__":
    new_site = Website("https://cnn.com")
    print(new_site.text)
    print("done")