# tests/test_analyzer.py
import pytest
from text_analyzer import TextAnalyzer

def test_empty_text_raises_error():
    empty_cases = [
        "",
        "   ", 
        "\n\t\r",
        " \t \n ",
    ]
    
    for text in empty_cases:
        with pytest.raises(ValueError):
            TextAnalyzer(text)

