from fastapi import FastAPI
from  text_analyzer import TextAnalyzer

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Speech Analyzer API"}

@app.post("/analyze")
async def analyze_text(text: str):
    analyzer = TextAnalyzer(text)
    analyzer.find_imperatives()
    analyzer.find_persons()
    analyzer.detect_questions()
    
    return {"result": analyzer.results}

"""
curl -X POST "http://127.0.0.1:8000/user" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "age": 25}'

`-X POST` - указываем метод
`-H "Content-Type: application/json"` - говорим серверу, что тело JSON
`-d '{"name": "Alice", "age": 25}'` - само тело запроса
"""