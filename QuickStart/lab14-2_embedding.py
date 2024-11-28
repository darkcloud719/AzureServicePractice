import os
import openai
from dotenv import load_dotenv
from rich import print as pprint

def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai.api_version = os.getenv("OPENAI_API_VERSION")
    openai.api_type = "azure"
    
    response = openai.embeddings.create(
        model = os.getenv("AZURE_OPENAI_DEPLOYMENT_FOR_EMBEDDINGS"),
        input = ["Apple"]
    )
    
    pprint(response.data[0].embedding)
    
if __name__ == "__main__":
    load_dotenv()
    main()