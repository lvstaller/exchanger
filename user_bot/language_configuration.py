import json


class LanguageConfiguration:
    def __init__(self, locale_path):
        self.locale_path = locale_path
        with open(locale_path, "r", encoding="utf-8") as j:
            self.locale_dict = json.load(j)

    def get_locale_text(self, locale, key):
        return self.locale_dict[locale][key]
