import logging
from pathlib import Path
from typing import Any, Dict, List

import razdel
import spacy

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

class Preprocessor:
    def __init__(self, text: str) -> None:
        """
        Initialize Preprocessor for TextAnalyzer

        Args:
            text: Raw text.
        """
        if not isinstance(text, str):
            raise TypeError(f"Expected string, got {type(text)}")
        self.text = text
        self.sentences = [_.text for _ in razdel.sentenize(self.text)]
        logger.info("Your text was already sentenized")
        self._spacy_model = None
        
        if self._spacy_model is None:
            try:
                self._spacy_model = spacy.load("ru_core_news_lg")
                logger.info(
                    "Spacy model loaded: lang=%s, name=%s",
                    self._spacy_model.meta.get("lang", "unknown"),
                    self._spacy_model.meta.get("name", "unknown")
                )
            except:
                logger.error("Failed to load spacy model. Install it: python -m spacy download ru_core_news_lg")

    def spacy_extract(self, sentence: str, features: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Extract tokens and entities using spaCy.

        Args:
            sentence: Sentences from the raw text.
            features: Dict of required features for tokens and entities.
                      For example: {"tokens": ["text", "pos", "span"], "ents": ["text", "span"]}

        Returns:
            Dict with "tokens" and "ents" features.
        """
        try:
            doc = self._spacy_model(sentence)
        except Exception as e:
            logger.error("Spacy processing failed for sentence: %r", sentence, exc_info=True)
            raise RuntimeError(f"Spacy error: {e}") from e
        
        out = {}

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
                if 'span' in requested:
                    t['span'] = (token.idx, token.idx + len(token.text))
                if 'morph' in requested:
                    t['morph'] = token.morph.to_dict()
                out['tokens'].append(t)

        if 'ents' in features and features['ents']:
            out['ents'] = []
            requested = features['ents']
            for ent in doc.ents:
                e = {}
                if 'text' in requested:
                    e['text'] = ent.text
                if 'label' in requested:
                    e['label'] = ent.label_
                if 'span' in requested:
                    e['span'] = (ent.start_char, ent.end_char)
                out['ents'].append(e)

        return out

