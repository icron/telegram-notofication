import nltk
from nltk.stem.snowball import SnowballStemmer, stopwords
from regex import regex

from app.parser.lang.en import English
from app.parser.lang.ru import Russian


class Parser:
    def __init__(self):
        self.__lemma = {
            "russian": Russian(),
            "english": English(),
        }

    @staticmethod
    def is_punctuation(token: str):
        punctuations = "?:!.,;"

        return token in punctuations

    @staticmethod
    def get_lang(string):
        # TODO using nltk detection
        has_cyrillic = regex.search(r'\p{IsCyrillic}', string)
        if has_cyrillic:
            return "russian"
        else:
            return "english"

    def parse(self, string: str, use_default_filter_pos: bool):
        # detect language
        lang = Parser.get_lang(string)

        # tokenization
        tokens = nltk.word_tokenize(string)

        # remove stop words and unnecessary symbols
        for token in tokens:
            if Parser.is_punctuation(token) or token in stopwords.words(lang):
                tokens.remove(token)

        # lemmatization and post stemming
        stemmer = SnowballStemmer(lang, ignore_stopwords=True)
        result = []

        default_filter_pos = None
        if use_default_filter_pos:
            default_filter_pos = self.__lemma[lang].get_default_filter_pos()

        for token in tokens:
            item = self.__lemma[lang].lemmatization(token, "NOUN", default_filter_pos)
            if item is not None:
                result.append(stemmer.stem(item).lower())

        return result
