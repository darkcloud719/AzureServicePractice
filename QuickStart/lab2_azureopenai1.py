import os,openai
from dotenv import load_dotenv
from rich import print as pprint

def main():

    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai.api_version = os.getenv("OPENAI_API_VERSION")
    openai.api_type = "azure"

    response = openai.chat.completions.create(
        model = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages = [
            {"role":"user","content":"What is the highest mountain in the world?"}
        ]
    )

    json = response.model_dump_json()

    

    pprint(response)

if __name__ == "__main__":
    load_dotenv()
    main()