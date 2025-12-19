import logging
from typing import Any

import razdel
import spacy

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
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
                    self._spacy_model.meta.get("name", "unknown"),
                )
            except Exception as e:
                logger.error("Failed to load spacy model 'ru_core_news_lg': %s", e)

    def spacy_extract(self, sentence: str, features: dict[str, list[str]]) -> dict[str, Any]:
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
            logger.exception("Spacy processing failed for sentence: %r", sentence)
            raise RuntimeError(f"Spacy error: {e}") from e

        out: dict[str, Any] = {}

        if features.get("tokens"):
            out["tokens"] = self._extract_tokens(doc, features["tokens"])
        if features.get("ents"):
            out["ents"] = self._extract_entities(doc, features["ents"])

        return out

    def _extract_tokens(self, doc, requested: list[str]) -> list[dict[str, Any]]:
        """
        Extract token-level features from a spaCy Doc.

        Args:
            doc: spaCy Doc object.
            requested: List of requested token attributes (e.g., ["text", "pos", "span"]).

        Returns:
            List of token dicts with requested fields.
        """
        tokens = []
        for token in doc:
            t = {}
            if "text" in requested:
                t["text"] = token.text
            if "pos" in requested:
                t["pos"] = token.pos_
            if "span" in requested:
                t["span"] = (token.idx, token.idx + len(token.text))
            if "morph" in requested:
                t["morph"] = token.morph.to_dict()
            tokens.append(t)
        return tokens

    def _extract_entities(self, doc, requested: list[str]) -> list[dict[str, Any]]:
        """
        Extract entity-level features from a spaCy Doc.

        Args:
            doc: spaCy Doc object.
            requested: List of requested entity attributes (e.g., ["text", "label", "span"]).

        Returns:
            List of entity dicts with requested fields.
        """
        entities = []
        for ent in doc.ents:
            e = {}
            if "text" in requested:
                e["text"] = ent.text
            if "label" in requested:
                e["label"] = ent.label_
            if "span" in requested:
                e["span"] = (ent.start_char, ent.end_char)
            entities.append(e)
        return entities
