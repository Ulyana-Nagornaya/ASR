from .data import AlignedTranscript, SpeakerDiarization, Transcript


class SpeakerAligner:
    """
    Совмещает транскрипцию и диаризацию методом максимального пересечения.
    """
    @staticmethod
    def align(
        transcript: Transcript,
        diarization: SpeakerDiarization,
        min_overlap_sec: float = 0.05
    ) -> AlignedTranscript:
        """
        Для каждого ASR-сегмента находит спикера с максимальным временным пересечением.
        """
        pass
