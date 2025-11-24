from typing import Optional
from .data import Transcript

class WhisperASR:
    """
    Обрабатывает аудио и возвращает нормализованный Transcript.
    """
    def __init__(
        self,
        model_name: str = "large-v3-turbo",
        device: str = "cuda",
        language: str = "ru"
    ):
        """
        Инициализирует модель Whisper.
        """
        pass

    def apply(self, audio_path: str) -> Transcript:
        """
        Применяет ASR к аудиофайлу.
        """
        pass