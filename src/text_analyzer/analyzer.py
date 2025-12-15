import logging

from typing import List

from .preprocessor import Preprocessor
from .constants import QUESTION_WORDS_PATH

from .data_models import SentenceResult

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

class TextAnalyzer(Preprocessor):
    def __init__(self,  text: str):
        super().__init__(text)
        self.results = [] 

        self.results: List[SentenceResult] = [
            SentenceResult(id=i, text=sent)
            for i, sent in enumerate(self.sentences, start=1)
        ]

    def find_imperatives(self, pos='VERB', tag_name='Mood', tag_value='Imp'):
        features = {'tokens': ['text', 'pos','morph','span']}
        for result in self.results:
            data = self.spacy_extract(result.text, features)
            imperatives = {}
            for t in data['tokens']:
                if t['pos'] == pos and t['morph'].get(tag_name) == tag_value:
                    imperatives[t['text']] = t['span']
            result.imperatives = imperatives 
        logger.info("Imperatives were extracted from the text")
        return self.results

    def find_persons(self):
        features = {'ents': ['text', 'label', 'span']}
        for result in self.results:
            data = self.spacy_extract(result.text, features)
            persons = {}
            for e in data['ents']:
                if e['label'] in ['PER', 'PERSON']:
                    persons[e['text']] = e['span']
            result.persons = persons
        logger.info("Name of the persons were extracted from the text")
        return self.results

    def load_question_words(self):
        try:
            if QUESTION_WORDS_PATH is None or (QUESTION_WORDS_PATH and not QUESTION_WORDS_PATH.exists()):
                raise FileNotFoundError(f"Question words file not found: {QUESTION_WORDS_PATH}")
            with open(QUESTION_WORDS_PATH, 'r', encoding='utf-8') as f:
                question_words = set(f.read().split(', '))
                return question_words
        except(OSError, UnicodeDecodeError) as e:
            logger.error("Failed to load question words: %s", e)

    def detect_questions(self):
        # Леммы!
        question_words = self.load_question_words()
        features = {'tokens': ['text']}
        for result in self.results:
            data = self.spacy_extract(result.text, features)
            found = [t['text'] for t in data['tokens'] if t['text'].lower() in question_words]
            is_general = '?' in result.text
            is_specific = bool(found) and is_general
            result.is_question = {
                "general question": is_general,
                "specific question": is_specific
            }
        logger.info("Questions were extracted from the text")
        return self.results