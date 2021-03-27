import pymorphy2

from app.parser.lang.interfaces import LangInterface


class Russian(LangInterface):
    def __init__(self):
        self.__analyzer = pymorphy2.MorphAnalyzer()

    def get_default_filter_pos(self):
        return ["NOUN", "LATN", "UNKN"]

    def lemmatization(self, word: str, preferable_pos="NOUN", filter_pos=None):
        parse_list = self.__analyzer.parse(word)
        normal_form = None
        for p in parse_list:
            if filter_pos is None or [i for i in filter_pos if i in p.tag]:
                normal_form = p.normal_form
                if preferable_pos in p.tag:
                    return normal_form

        return normal_form
