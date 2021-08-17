import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from src.application.text_preprocessing import TextPreprocessing
from src.application.main import get_prediction


cleaner = TextPreprocessing()


def test_text_preprocessing():
    assert 'ветер' == cleaner.text_preprocessing('ветер! ()@@')


def test_bert():
    assert ('Toxic', 0.9210994243621826) == get_prediction('как дам тебе в лоб')
