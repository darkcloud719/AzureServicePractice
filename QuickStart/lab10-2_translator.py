import os,json,sys
from dotenv import load_dotenv
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError

def main():

    key = os.getenv("AZURE_TRANSLATOR_KEY")
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    region = os.getenv("AZURE_TRANSLATOR_REGION")
    credential = AzureKeyCredential(key)
    
    text_translator = TextTranslationClient(endpoint=endpoint, credential=credential, region=region)

    try:
        source_language = "en"
        target_language = ["zh-Hant","ja"]
        input_text_elements = [InputTextItem(text="This is a test")]

        response = text_translator.translate(body=input_text_elements, to_language=target_language, from_language=source_language)
        translation = response[0] if response else None
        if translation:
            for translated_text in translation.translations:
                print(f"Text was translated to : '{translated_text.to}' and the result is: '{translated_text.text}'")
    except HttpResponseError as exception:
        print(f"Error Code:{exception.error.code}")
        print(f"Message:{exception.error.message}")          

if __name__ == "__main__":
    load_dotenv()
    main()
