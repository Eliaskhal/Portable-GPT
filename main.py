from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
import os
import time

load_dotenv()
api_key = os.getenv("API_KEY")

console = Console()
greeting_text = """# \033[1;36mCodeCraft Assistant\033[0m

\033[1;32mWelcome to CodeCraft!\033[0m Your terminal coding companion for \033[1;33mswift code generation\033[0m, \033[1;31mbug fixes\033[0m, \033[1;34mcode reviews\033[0m, \033[1;35mconcept explanations\033[0m, and \033[1;37mcustom coding assistance\033[0m. Let's \033[1;34mc\033[1;33mr\033[1;32ma\033[1;31mf\033[1;35mt\033[1;37m your code seamlessly!\n
"""
markdown_text = Markdown(greeting_text)
console.print(markdown_text)

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
    content=console.input("[red]You: [/red]")
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
    
    assistant_response = Markdown("""\n\033[1;32mAssitant: \033[0m {}\n""".format(new_message))
    console.print(assistant_response)
