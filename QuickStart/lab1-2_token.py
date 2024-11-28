import os, openai
from dotenv import load_dotenv
from rich import print as pprint

def main():
    
    assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY is not set"
    assert os.getenv("AZURE_OPENAI_ENDPOINT"), "AZURE_OPENAI_ENDPOINT is not set"
    assert os.getenv("OPENAI_API_VERSION"), "OPENAI_API_VERSION is not set"
    assert os.getenv("AZURE_OPENAI_DEPLOYMENT"), "AZURE_OPENAI_DEPLOYMENT is not set"

    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai.api_version = os.getenv("OPENAI_API_VERSION")
    openai.api_type = "azure"

    response = openai.chat.completions.create(
        model = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages = [
            {"role":"system", "content":"You are a helpful assistant."},
            {"role":"user", "content":"Please write a poem of 200 words that relates to the theme of nature."}
        ],
        max_tokens=20
    )

    
    pprint(response.choices[0].message.content)

if __name__ == "__main__":
    load_dotenv()
    main()
