from pydantic import BaseModel, Field


class SentenceResult(BaseModel):
    """Results of text analyzing for each sentence."""

    # В докстринг лучше еще добавить описание каждого поля.

    id: int
    text: str
    persons: dict[str, tuple[int, int]] | None = Field(default=None)
    imperatives: dict[str, tuple[int, int]] | None = Field(default=None)
    is_question: dict[str, bool] | None = Field(default=None)
