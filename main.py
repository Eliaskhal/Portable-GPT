from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

client = OpenAI(api_key=api_key)

with open('prompt.txt', 'r') as f:
    prompt = f.read()

assistant = client.beta.assistants.create(
    name="Terminal GPT",
    instructions=prompt,
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-turbo-preview"
)