import json


class Translation:
    def __init__(self, translation_file):
        with open(translation_file, 'r', encoding='utf-8') as file:
            self.translations = json.load(file)

    def get_translation(self, key, language="IT", **kwargs):
        translation = self.translations.get(language, {}).get(key, key)
        return translation.format(**kwargs)


translator = Translation('app/translations/translations.json')
