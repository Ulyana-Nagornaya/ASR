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
    analyzer = TextAnalyzer(text)
    analyzer.find_imperatives()
    analyzer.find_persons()
    analyzer.detect_questions()

    return {"result": analyzer.results}
