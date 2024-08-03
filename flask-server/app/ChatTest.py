import pathlib
import textwrap
import os
import google.generativeai as genai
import argparse
from IPython.display import display
from IPython.display import Markdown
import re
from dotenv import load_dotenv


load_dotenv()
GEMINI_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GEMINI_KEY)

model = genai.GenerativeModel('gemini-1.5-pro')

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

def talk_to_bot(userInput):
    chat = model.start_chat(history=[])
    response = chat.send_message(userInput)
    text = to_markdown(response.text)
    return text    
    
def extract_titles(text):
   # Find all matches of patterns like "1. ", "2. ", etc.
    matches = list(re.finditer(r'\d+\.\s+', text))
    if not matches:
        return [text.strip()]

    # Split the text based on these matches
    titles = []
    start = 0
    for match in matches:
        end = match.start()
        if end > start:
            titles.append(text[start:end].strip())
        start = match.start()
    # Append the last segment
    titles.append(text[start:].strip())

    # Clean titles: Remove '>', '\n', leading numeric prefixes, and extra spaces
    cleaned_titles = []
    for title in titles:
        # Remove unwanted characters and leading/trailing spaces
        cleaned = title.replace('>', '').replace('\n', '').strip()
        # Remove leading numeric prefixes like '1. ', '2. ', etc.
        cleaned = re.sub(r'^\d+\.\s*', '', cleaned)
        if cleaned:  # Only add non-empty titles
            cleaned_titles.append(cleaned)
    
    return cleaned_titles

if __name__ =="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs",nargs='+', help="Input text of the chatbot")
    args = vars(ap.parse_args())
    
    conversation_history = []
    
       # Process each input and collect responses
    for user_input in args["inputs"]:
        response_text = talk_to_bot(user_input)
        # Extract titles from the response
        titles = extract_titles(response_text)
        # Append each title to the conversation history
        conversation_history.extend(titles)
    
    # Print the conversation history
    for i, entry in enumerate(conversation_history):
        print(f"Title {i+1}: {entry}")
    
    