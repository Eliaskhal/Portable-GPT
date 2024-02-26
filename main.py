from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()
api_key = os.getenv("API_KEY")

client = OpenAI(api_key=api_key)

with open('prompt.txt', 'r') as f:
    prompt = f.read()

assistant = client.beta.assistants.create(
    name="Terminal GPT",
    instructions=prompt,
    tools=[{"type": "code_interpreter"}],
    model="gpt-3.5-turbo"
)

thread = client.beta.threads.create()

while True:
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=input()
    )
    
    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    )
    
    while run.status != "completed":
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value
    
    print(new_message)