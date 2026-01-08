from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
INTERROGATIVE_WORDS_PATH = PROJECT_ROOT / "assets" / "word lists" / "interrogative words.txt"
# Советую "собирать" путь вот так: Path(PROJECT_ROOT, "assets", "word lists", "interrogative words.txt")
# Это абсолютный аналог вашего варианта, но зато так вы избежите путаницы из-за неоднозначности символа `/`.

# Вы молодец, что вынесли INTERROGATIVE_WORDS_PATH в константы!
