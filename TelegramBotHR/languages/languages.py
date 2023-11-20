import json


def get_languages_data():
    with open('languages/languages.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    return json_data
