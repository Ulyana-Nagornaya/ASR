from .analyzer import TextAnalyzer
from .constants import INTERROGATIVE_WORDS_PATH
from .data_models import SentenceResult
from .preprocessor import Preprocessor

__all__ = [
    "INTERROGATIVE_WORDS_PATH",  # Не используется "снаружи" -> не должно быть доступно юзеру (инкапсуляция)
    "Preprocessor",  # Используется только в тестах. Тоже не должно быть доступно юзеру (инкапсуляция)
    "SentenceResult",
    "TextAnalyzer",
]
