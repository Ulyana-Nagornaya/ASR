from .data import SpeakerDiarization


class PyannoteDiarizer:
    """
    Обрабатывает аудио и возвращает SpeakerDiarization.
    """
    def __init__(
        self,
        model_name: str = 'pyannote/speaker-diarization-3.1',
        auth_token: str = None,
        device: str = 'cuda'
    ):
        """
        Инициализирует диаризатор.
        """
        pass

    def apply(self, audio_path: str) -> SpeakerDiarization:
        """
        Применяет диаризацию к аудиофайлу.
        """
        pass
