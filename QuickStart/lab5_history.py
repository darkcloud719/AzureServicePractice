import os
import openai
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_type = "azure"

all_hist = []

console = Console()

def chat(user_msg):
    global all_hist
    message = [{"role":"user","content":user_msg}]
    all_hist.append({"role":"user","content":user_msg})

    response_content = get_reply(message)
    print(response_content)
    all_hist.append({"role":"assistant","content":response_content})

def get_reply(message):
    try:
        response = openai.chat.completions.create(
            model = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages = message
        )
        return response.choices[0].message.content
    except openai.APIError as err:
        reply = f"Error {err.message}"
        print(reply)
        console.print(reply, sytle="bold red")

def print_history(history):
    table = Table(title="Chat History", style="cyan")
    table.add_column("Role", justify="left", style="magenta")
    table.add_column("Content", justify="left", style="green")

    for item in history:
        table.add_row(item["role"], item["content"])

    console.print(table)

def main():
    while True:
        msg = input("You: ")
        if not msg.strip():
            break
        chat(msg)
        print("\n")
    
    print_history(all_hist)

if __name__ == "__main__":
    main()