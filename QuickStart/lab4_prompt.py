import openai
import os
from dotenv import load_dotenv

def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai.api_version = os.getenv("OPENAI_API_VERSION")
    openai.api_type = "azure"

    response = openai.chat.completions.create(
        model = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages = [
            {"role":"system","content":"You are a professional translator. Your task is to translate any English text accurate and natural Mandarin Chinese."},
            {"role":"user","content":"What is the highest mountain in the world?"}
        ]
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    load_dotenv()
    main()