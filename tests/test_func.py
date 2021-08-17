import sys, os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from src.application.text_preprocessing import TextPreprocessing


cleaner = TextPreprocessing()


def test_text_preprocessing():
    assert 'ветер' == cleaner.text_preprocessing('ветер! ()@@')
