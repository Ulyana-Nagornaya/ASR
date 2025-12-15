from pathlib import Path

from text_analyzer.analyzer import TextAnalyzer

PROJECT_ROOT = Path(__file__).parent.parent.parent
EXAMPLE_PATH = PROJECT_ROOT / 'assets' / 'data' / 'example.txt'


def main():
    with open(EXAMPLE_PATH, 'r', encoding='utf-8') as f:
        data = f.read()

    text = TextAnalyzer(data)

    text.find_imperatives()
    text.find_persons()
    text.detect_questions()
    print(text.results)

if __name__ == '__main__':
    main()
