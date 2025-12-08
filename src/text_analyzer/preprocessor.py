import spacy 
 #python -m spacy download ru_core_news_lg
import razdel

class Preprocessor:
    def __init__(self, text):
        self.text = text
        self._sentences = [_.text for _ in razdel.sentenize(self.text)]
        self.spacy_model = spacy.load("ru_core_news_lg")

    def spacy_extract(self, sentence, features):
        doc = self.spacy_model(sentence)
        out = {}

        # Токены
        if 'tokens' in features and features['tokens']:
            out['tokens'] = []
            requested = features['tokens']
            for token in doc:
                t = {}
                if 'text' in requested:
                    t['text'] = token.text
                if 'lemma' in requested:
                    t['lemma'] = token.lemma_
                if 'pos' in requested:
                    t['pos'] = token.pos_
                if 'idx' in requested:
                    t['idx'] = token.idx
                if 'morph' in requested:
                    t['morph'] = token.morph.to_dict()
                out['tokens'].append(t)

        # Сущности
        if 'ents' in features and features['ents']:
            out['ents'] = []
            requested = features['ents']
            for ent in doc.ents:
                e = {}
                if 'text' in requested:
                    e['text'] = ent.text
                if 'label' in requested:
                    e['label'] = ent.label_
                if 'start_char' in requested:
                    e['start_char'] = ent.start_char
                if 'end_char' in requested:
                    e['end_char'] = ent.end_char
                out['ents'].append(e)

        return out

