import json

class LanguageConfiguration():
    def __init__(self,locale_path):
        self.locale_path = locale_path
        self.locale_dict = json.load(locale_path)

    def get_locale_text(self,locale,key):
        return self.locale_dict[locale][key]