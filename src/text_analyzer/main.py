from text_analyzer import Text_Analyzer
from constants import DATA_PATH, EXAMPLE_PATH

def main():
    with open(EXAMPLE_PATH, 'r', encoding='utf-8') as f:
        data = f.read()

    text = Text_Analyzer(data)

    text.find_imperatives()
    text.find_persons()
    text.detect_questions()
    print(text.results)

if __name__ == "__main__":
    main()
