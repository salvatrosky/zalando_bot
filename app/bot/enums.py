from enum import Enum


class LanguagesEnum(Enum):
    EN = "English"
    IT = "Italiano"
    ES = "Español"

    @classmethod
    def choices(cls):
        return [(tag.name, tag.value) for tag in cls]

class EventTypesEnum(Enum):
    LANGUAGE_SET = "LANGUAGE_SET"