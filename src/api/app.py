from fastapi import FastAPI

from text_analyzer import SentenceResult, TextAnalyzer

app = FastAPI()


@app.get("/")
async def read_root() -> dict[str, str]:
    """Welcome endpoint."""
    return {"message": "Speech Analyzer API"}


@app.post("/analyze")
async def analyze_text(text: str) -> dict[str, list[SentenceResult]]:
    """Run linguistic analysis."""
    # Текст лучше принимать в теле запроса. Для этого нужно добавить Pydantic-модель и передавать текст в JSON.
    # Бонусом curl не будет кодировать русский текст, и API будет заранее готов к расширению новыми входными полями.
    # Вы, возможно, даже заметили, что если отправлять запрос через Swagger UI,
    # вы будете получать что-то вроде `http://127.0.0.1:8000/analyze?text=%D0%90%...`.
    # Вот это как раз из-за того, что у вас нет Pydantic-модели

    # Пример модели:
    # class AnalyzeRequest(BaseModel):
    #     text: str

    analyzer = TextAnalyzer(text)
    analyzer.find_imperatives()
    analyzer.find_persons()
    analyzer.detect_questions()

    return {"result": analyzer.results}
