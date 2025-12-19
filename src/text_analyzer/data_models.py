from typing import Dict, Optional, Tuple

from pydantic import BaseModel, Field


class SentenceResult(BaseModel):
    """
    Results of text analyzing for each sentence.
    """
    id: int
    text: str
    persons: Optional[Dict[str, Tuple[int, int]]] = Field(default=None)
    persons: Optional[Dict[str, Tuple[int, int]]] = Field(default=None)
    imperatives: Optional[Dict[str, Tuple[int, int]]] = Field(default=None)
    is_question: Optional[Dict[str, bool]] = Field(default=None)