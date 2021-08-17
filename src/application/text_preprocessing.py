import pymorphy2
import re


class TextPreprocessing:
    """Preprocessing and lemmatization text

    """
    def __init__(self):
        # Lemmatizer
        self.morph = pymorphy2.MorphAnalyzer()
    
    def text_preprocessing(self, text: str) -> str:
        """Lemmatizing and preprocessing input text

        :param text: input "raw" tex
        :return: preprocessing text
        """
        stop_words = [
            'и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то',
           'все', 'она', 'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по',
           'только', 'ее', 'мне', 'было', 'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему',
           'теперь', 'когда', 'даже', 'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'ни', 'быть',
           'был', 'него', 'до', 'вас', 'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом',
           'себя', 'ничего', 'ей', 'может', 'они', 'тут', 'где', 'есть', 'надо', 'ней', 'для',
           'мы', 'тебя', 'их', 'чем', 'была', 'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже',
           'себе', 'под', 'будет', 'ж', 'тогда', 'кто', 'этот', 'того', 'потому', 'этого', 'какой',
           'совсем', 'ним', 'здесь', 'этом', 'один', 'почти', 'мой', 'тем', 'чтобы', 'нее', 'сейчас',
           'были', 'куда', 'зачем', 'всех', 'никогда', 'можно', 'при', 'наконец', 'два', 'об', 'другой',
           'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про', 'всего', 'них',
           'какая', 'много', 'разве', 'три', 'эту', 'моя', 'впрочем', 'хорошо', 'свою', 'этой', 'перед',
           'иногда', 'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более', 'всегда', 'конечно', 'всю',
        ]
        text = re.sub(re.compile(r"<[^>]*>"), " ", text)
        text = re.sub(re.compile(r"^\[id\d*|.*\],*\s*"), "", text)
        text = re.sub(re.compile(r"(&quot;)|(&lt;)|(&gt;)|(&amp;)|(&apos;)"), " ", text)
        text = re.sub(re.compile(
            r"https?://(www\.)?[-a-zA-Z0-9@:%._+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_+.~#?&/=]*)")," ", text)
        text = re.sub(re.compile(r"\[[^\[\]]+\|([^\[\]]+)\]"), r"\1", text)
        text = re.sub(re.compile(r"(&#\d+;)"), " ", text)
        text = re.sub(re.compile(r"[(_#*=^/`@«»©…“•—<>\[\]\"'+%|&]"), " ", text)
        text = re.sub(re.compile(r"[.,!?\;:)(_#*=^/`@«»©…“•—<>\[\]\"'+%|&]"), " ", text)
        text = text.replace("  ", " ")
        text = text.replace("--", " ")
        text = text.replace('\n', ' ')
        text = re.sub("\s\s+", " ", text)
        return ' '.join(
            [self.morph.parse(word)[0].normal_form for word in text.lower().split() if word not in stop_words])
