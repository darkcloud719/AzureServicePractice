import os
import openai
from dotenv import load_dotenv
from rich import print as pprint

def main():

    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai.api_version = os.getenv("OPENAI_API_VERSION")
    openai.api_type = "azure"

    response = openai.chat.completions.create(
        model = os.getenv("AZURE_OPENAI_DEPLOYMENT_FOR_VISION"),
        messages = [
            {"role":"system","content":"You are a helpful assistant."},
            {"role":"user","content":[
                {"type":"text","text":"Please describe this image"},
                {"type":"image_url","image_url":{"url":"https://flagtech.github.io/F3762/images/cat1.jpg"}}
            ]}
        ],
        max_tokens=100
    )

    pprint(response.choices[0].message.content)

if __name__ == "__main__":
    load_dotenv()
    main()