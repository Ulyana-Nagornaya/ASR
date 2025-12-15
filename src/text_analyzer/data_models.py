from typing import Dict, Optional, Tuple

from pydantic import BaseModel


class SentenceResult(BaseModel):
    """
    Results of text analyzing for each sentence.
    """
    id: int
    text: str
    persons: Optional[Dict[str, Tuple[int, int]]] = None
    imperatives: Optional[Dict[str, Tuple[int, int]]] = None
    is_question: Optional[Dict[str, bool]] = None
