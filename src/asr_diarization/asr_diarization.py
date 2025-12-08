from typing import Dict

from .data import AlignedTranscript


class SeminarASRPipeline:
    """
    Основной пайплайн для обработки семинаров:
    1. ASR (Whisper)
    2. Диаризация (PyAnnote)
    3. Совмещение (SpeakerAligner)
    """
    def __init__(
        self,
        asr_model: str = 'large-v3-turbo',
        diarization_model: str = 'pyannote/speaker-diarization-3.1',
        hf_token: str = None,
        device: str = 'cuda'
    ):
        """
        Инициализирует компоненты пайплайна.
        """
        pass

    def run(self, audio_path: str) -> AlignedTranscript:
        """
        Запускает полную обработку аудио.
        """
        pass

    def export_json(self, aligned: AlignedTranscript) -> Dict:
        """
        Экспортирует результат в JSON-совместимый dict.
        """
        pass
