import os
import openai
from dotenv import load_dotenv
from rich import print as pprint
from openai import AzureOpenAI

def main():
    
    client = AzureOpenAI(
        api_key = os.getenv("OPENAI_API_KEY"),
        api_version = os.getenv("OPENAI_API_VERSION"),
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    
    response = client.embeddings.create(
        model = os.getenv("AZURE_OPENAI_DEPLOYMENT_FOR_EMBEDDINGS"),
        input = "Apple"
    )
    
    pprint(response.data[0].embedding)
    
if __name__ == "__main__":
    load_dotenv()
    main()