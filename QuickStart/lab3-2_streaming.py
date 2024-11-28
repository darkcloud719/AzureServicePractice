import os,openai,asyncio
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv

async def main():

    client = AsyncAzureOpenAI(
        api_key = os.getenv("OPENAI_API_KEY"),
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version = os.getenv("OPENAI_API_VERSION")
    )

    response = await client.chat.completions.create(
        model = os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages = [
            {"role":"system","content":"You are a helpful assistant."},
            {"role":"user","content":"Please write a poem of 100 words that relates to the theme of nature."}
        ],
        stream=True
    )

    async for chunk in response:
        if chunk.choices and chunk.choices[0].delta:
            print(chunk.choices[0].delta.content or "", end="")

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main()) 