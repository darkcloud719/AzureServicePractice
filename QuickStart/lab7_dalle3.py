import os,requests,json,openai
from dotenv import load_dotenv
from PIL import Image

def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai.api_version = os.getenv("OPENAI_API_VERSION")
    openai.api_type = "azure"

    result = openai.images.generate(
        model = "dall-e-3",
        prompt = "一個人穿著黑色西裝戴墨鏡在河邊跑步",
        n = 1
    )

    # json_response = json.loads(result.model_dump_json())

    image_dir = os.path.join(os.curdir,"images")

    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    image_path = os.path.join(image_dir,"generated_image2.png")

    image_url = result.data[0].url
    generated_image = requests.get(image_url).content
    with open(image_path,"wb") as image_file:
        image_file.write(generated_image)
    image = Image.open(image_path)
    image.show()

if __name__ == "__main__":
    load_dotenv()
    main()
