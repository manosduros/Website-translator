import os
from bs4 import BeautifulSoup
import requests


API_KEY = os.environ.get("GOOGLE_API_KEY")
TRANSLATION_ENDPOINT = "https://translation.googleapis.com/language/translate/v2"
TARGET_LANGUAGE = "hi"
DIRECTORY_FOLDER = "C:/Downloaded Web Sites/www.classcentral.com"


def get_text_elements(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        website_html = file.read()
    soup = BeautifulSoup(website_html, "html.parser")
    text_elements = [element.get_text().strip() for element in soup.find_all(text=True) if element.get_text().strip()]
    return text_elements


def write_translated_html_file(file_path, translated_text_elements):
    with open(file_path, mode="r", encoding="utf-8") as file:
        website_html = file.read()
    soup = BeautifulSoup(website_html, "html.parser")
    for element in soup.find_all(text=True):
        if element.strip() in translated_text_elements:
            element.replace_with(translated_text_elements[element.strip()])
    translated_html = str(soup)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(translated_html)
        

for root, dirs, files in os.walk(DIRECTORY_FOLDER):
    for file in files:
        if file.endswith(".html") or file.endswith(".htm"):
            file_path = os.path.join(root, file)
            sentences = get_text_elements(file_path)
            translated_sentences = dict()

            for sentence in sentences:
                parameters = {
                    "q": sentence,
                    "target": TARGET_LANGUAGE,
                    "key": API_KEY,
                }
                response = requests.post(TRANSLATION_ENDPOINT, params=parameters)
                translated_sentence = response.json()["data"]["translations"][0]["translatedText"]
                translated_sentences[sentence] = translated_sentence
                write_translated_html_file(file_path, translated_sentences)

