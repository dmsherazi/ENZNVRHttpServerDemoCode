import os
import json
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source='auto', target='en')

def translate_text(text):
    return translator.translate(text)

def translate_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    def translate_data(data):
        if isinstance(data, dict):
            return {k: translate_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [translate_data(item) for item in data]
        elif isinstance(data, str):
            return translate_text(data)
        else:
            return data

    translated_data = translate_data(data)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(translated_data, file, ensure_ascii=False, indent=4)

def translate_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            print("Translating {}...".format(filename))
            translate_json_file(file_path)
            print("{} translated.".format(filename))

if __name__ == "__main__":
    folder_path = input("Enter the folder path containing JSON files: ")
    translate_folder(folder_path)
    print("All files translated.")
