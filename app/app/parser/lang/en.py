import spacy

from app.parser.lang.interfaces import LangInterface


class English(LangInterface):
    def __init__(self):
        self.__analyzer = spacy.load("en_core_web_sm")

    def get_default_filter_pos(self):
        return ["NOUN", "INTJ", "PROPN", "PRON", "X"]

    def lemmatization(self, word: str, preferable_pos="NOUN", filter_pos=None):
        doc = self.__analyzer(word)
        for token in doc:
            if filter_pos is None or [i for i in filter_pos if i == token.pos_]:
                return token.lemma_
