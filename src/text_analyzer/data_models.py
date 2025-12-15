from typing import Dict, Tuple, Optional
from pydantic import BaseModel, Field

class SentenceResult(BaseModel):
    id: int
    text: str
    persons: Dict[str, Tuple[int, int]] = Field(default_factory=dict)
    imperatives: Dict[str, Tuple[int, int]] = Field(default_factory=dict)
    is_question: Optional[Dict[str, bool]] = None