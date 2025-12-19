import logging
import re
from typing import List, Set

from .constants import INTERROGATIVE_WORDS_PATH
from .data_models import SentenceResult
from .preprocessor import Preprocessor

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

class TextAnalyzer(Preprocessor):
    """
    Text analyzer for russian texts.
    """
    def __init__(self, text: str) -> None:
        """
        Initialize Analyzer and create SentenceResult.

        Args:
            text: Raw text for analyzing.
        """
        if not text or not re.search(r"\S", text):
            raise ValueError("Text is empty or whitespace only")
        
        super().__init__(text)
        self.results: List[SentenceResult] = [
            SentenceResult(id=i, text=sent)
            for i, sent in enumerate(self.sentences, start=1)
        ]
        logger.info('TextAnalyzer is ready')


    def find_imperatives(
        self,
        pos: str = 'VERB',
        tag_name: str = 'Mood',
        tag_value: str = 'Imp'
    ) -> List[SentenceResult]:
        """
        Extract imperatives.

        Args:
            pos: pos tag ("VERB" by default).
            tag_name: name of morphological feature ("Mood" by default).
            tag_value: value of the feature ("Imp" by default).

        Returns:
            TextAnalyzer's results with extracted imperatives for each sentence.
        """
        features = {'tokens': ['text', 'pos','morph','span']}
        for result in self.results:
            data = self.spacy_extract(result.text, features)
            imperatives = {}
            for t in data['tokens']:
                if t['pos'] == pos and t['morph'].get(tag_name) == tag_value:
                    imperatives[t['text']] = t['span']
            result.imperatives = imperatives
        logger.info('Imperatives were extracted from the text')
        return self.results

    def find_persons(self) -> List[SentenceResult]:
        """
        Extract personal names.

        Returns:
            TextAnalyzer's results with extracted personal names for each sentence.
        """
        features = {'ents': ['text', 'label', 'span']}
        for result in self.results:
            data = self.spacy_extract(result.text, features)
            persons = {}
            for e in data['ents']:
                if e['label'] in ['PER', 'PERSON']:
                    persons[e['text']] = e['span']
            result.persons = persons
        logger.info('Personal names were extracted from the text')
        return self.results

    def load_interrogative_words(self) -> Set[str]:
        """
        Load the list of interrogative words.

        Returns:
            Set of interrogative words.
        """
        try:
            if INTERROGATIVE_WORDS_PATH is None or (INTERROGATIVE_WORDS_PATH and not INTERROGATIVE_WORDS_PATH.exists()):
                raise FileNotFoundError(f'Question words file not found: {INTERROGATIVE_WORDS_PATH}')
            with open(INTERROGATIVE_WORDS_PATH, 'r', encoding='utf-8') as f:
                return set(f.read().split(', '))
        except(OSError, UnicodeDecodeError) as e:
            logger.error('Failed to load question words: %s', e)

    def detect_questions(self) -> List[SentenceResult]:
        """
        Detect types of questions (general or special).

        Returns:
            TextAnalyzer's results with extracted question types.
        """
        question_words = self.load_interrogative_words()
        features = {'tokens': ['text']}
        for result in self.results:
            data = self.spacy_extract(result.text, features)
            found = [t['text'] for t in data['tokens'] if t['text'].lower() in question_words]
            is_general = '?' in result.text
            is_specific = bool(found) and is_general
            result.is_question = {
                'general question': is_general,
                'specific question': is_specific
            }
        logger.info('Questions were extracted from the text')
        return self.results
