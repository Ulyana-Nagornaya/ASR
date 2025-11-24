from dataclasses import dataclass, field
from typing import List, Optional, Set
from collections import defaultdict

class AudioSegment:
    """
    Неизменяемый сегмент аудио
    """

    start: float
    end: float
    speaker: Optional[str] = None
    text: Optional[str] = None
    confidence: Optional[float] = None

    # TODO: добавить валидацию

    @property
    def duration(self) -> float:
        # TODO: вернуть разность end - start
        pass

@dataclass
class Transcript:
    """
    Результат ASR: текстовые сегменты
    """
    segments: List[AudioSegment]
    language: str = "ru"

    # TODO: отсортировать сегменты по start и проверить пересечения

@dataclass
class SpeakerDiarization:
    """
    Результат диаризации: временные сегменты со спикерами, без текста.
    """
    segments: List[AudioSegment]
    num_speakers: int = -1

    # TODO: отсортировать сегменты по start и 
        #   2. собрать уникальные speaker (игнорируя None)
        #   3. установить self.num_speakers = len(уникальных)
        #   → использовать object.__setattr__(self, 'num_speakers', value), чтобы избежать рекурсии
    
@dataclass
class AlignedTranscript:
    """
    Финальный результат: транскрипция с привязкой к спикерам.
    """
    segments: List[AudioSegment]

    @property
    def speakers(self) -> Set[str]:
        # TODO: вернуть множество всех спикеров
        pass
    
    def to_json(self) -> dict:
        # TODO: собрать список словарей и вернуть json
        pass

    def get_speaker_text(self, speaker_id: str) -> str:
        # TODO: собрать тексты спикеров
        pass