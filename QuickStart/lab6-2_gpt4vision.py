import os,openai,base64
from rich import print as pprint
from dotenv import load_dotenv

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai.api_version = os.getenv("OPENAI_API_VERSION")
    openai.api_type = "azure"

    img = encode_image("cat.jpg")

    response = openai.chat.completions.create(
        model = os.getenv("AZURE_OPENAI_DEPLOYMENT_FOR_VISION"),
        messages = [
            {"role":"system","content":"You are a helpful assistant."},
            {"role":"user","content":[
                {"type":"text","text":"Please describe this image"},
                {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{img}",}}
            ]}
        ],
        max_tokens=100
    )

    pprint(response.choices[0].message.content)

if __name__ == "__main__":
    load_dotenv()
    main()