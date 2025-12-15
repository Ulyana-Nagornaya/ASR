import logging

from .preprocessor import Preprocessor
from .constants import QUESTION_WORDS_PATH

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

class TextAnalyzer(Preprocessor):
    def __init__(self, sentences):
        super().__init__(sentences)
        self.results = [] 

        for sent_idx, sentence in enumerate(self.sentences, 1):
            self.results.append({sent_idx: sentence})

    def _get_sentence(self, sent_dict):
        for key, value in sent_dict.items():
            if isinstance(key, int) and isinstance(value, str):
                return value
        logger.error("No sentence found in sent_dict")

    def find_imperatives(self, pos='VERB', tag_name='Mood', tag_value='Imp'):
        features = {'tokens': ['text', 'pos','morph','span']}
        for sent_dict in self.results:
            sentence = self._get_sentence(sent_dict)
            data = self.spacy_extract(sentence, features)
            imperatives = {}
            for t in data['tokens']:
                if t['pos'] == pos and t['morph'].get(tag_name) == tag_value:
                    imperatives[t['text']] = t['span']
            sent_dict['imperatives'] = imperatives
        logger.info("Imperatives were extracted from the text")
        return self.results

    def find_persons(self):
        features = {'ents': ['text', 'label', 'span']}
        for sent_dict in self.results:
            sentence = self._get_sentence(sent_dict)
            data = self.spacy_extract(sentence, features)
            persons = {}
            for e in data['ents']:
                if e['label'] in ['PER', 'PERSON']:
                    persons[e['text']] = e['span']
            sent_dict['persons'] = persons
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
        for sent_dict in self.results:
            sentence = self._get_sentence(sent_dict)
            data = self.spacy_extract(sentence, features)

            is_question = {}
            is_general = '?' in sentence
    
            found = [t['text'] for t in data['tokens'] if t['text'].lower() in question_words]

            is_specific = bool(found) and is_general
            
            is_question["general question"] = is_general
            is_question["specific question"] = is_specific
            sent_dict["is_question"] = is_question
        logger.info("Questions were extracted from the text")
        return self.results