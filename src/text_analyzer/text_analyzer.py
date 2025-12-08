from preprocessor import Preprocessor
from constants import QUESTION_WORDS_PATH

class Text_Analyzer(Preprocessor):
    def __init__(self, _sentences):
        super().__init__(_sentences)
        self.results = [] 

        for sent_idx, sentence in enumerate(self._sentences, 1):
            self.results.append({sent_idx: sentence})

    def _get_sentence(self, sent_dict):
        for key, value in sent_dict.items():
            if isinstance(key, int) and isinstance(value, str):
                return value

    def find_imperatives(self, pos='VERB', tag_name='Mood', tag_value='Imp'):
        features = {'tokens': ['text', 'pos', 'idx', 'morph']}
        for sent_dict in self.results:
            sentence = self._get_sentence(sent_dict)
            data = self.spacy_extract(sentence, features)
            imperatives = {}
            for t in data['tokens']:
                if t['pos'] == pos and t['morph'].get(tag_name) == tag_value:
                    imperatives[t['text']] = t['idx']
            sent_dict['imperatives'] = imperatives
        return self.results

    def find_persons(self):
        features = {'ents': ['text', 'label', 'start_char']}
        for sent_dict in self.results:
            sentence = self._get_sentence(sent_dict)
            data = self.spacy_extract(sentence, features)
            persons = {}
            for e in data['ents']:
                if e['label'] in ['PER', 'PERSON']:
                    persons[e['text']] = e['start_char']
            sent_dict['persons'] = persons
        return self.results

    def load_question_words(self):
        with open(QUESTION_WORDS_PATH, 'r', encoding='utf-8') as f:
            question_words = set(f.read().split(', '))
        return question_words

    def detect_questions(self):
        # Леммы!
        question_words = self.load_question_words()
        features = {'tokens': ['text']}
        for sent_dict in self.results:
            sentence = self._get_sentence(sent_dict)
            data = self.spacy_extract(sentence.lower(), features)

            is_question = {}
            is_general = '?' in sentence
    
            found = [t['text'] for t in data['tokens'] if t['text'] in question_words]

            is_specific = bool(found) and is_general
            
            is_question["general question"] = is_general
            is_question["specific question"] = is_specific
            sent_dict["is_question"] = is_question

        return self.results