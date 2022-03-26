import pytest

from src.application.classifier.text_preprocessing import text_preprocessing


@pytest.mark.parametrize("test_input,expected", [(' ветер ()@@', 'ветер'),
                                                 ('«mouse»©', 'mouse')])
def test_text_preprocessing(test_input, expected) -> None:
    """Test for text preprocessing function.

    @param test_input: input test raw string
    @param expected: expected clean string
    """
    assert text_preprocessing(test_input) == expected
