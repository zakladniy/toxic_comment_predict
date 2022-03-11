import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(
    inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from src.application.text_preprocessing import text_preprocessing


def test_text_preprocessing() -> None:
    """Test for text preprocessing function."""
    assert 'ветер' == text_preprocessing('ветер ()@@')
