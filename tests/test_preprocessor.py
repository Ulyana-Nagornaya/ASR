from text_analyzer.preprocessor import Preprocessor
# Вы вынесли `Preprocessor` в `src/text_analyzer/__init__.py`, поэтому можете импортировать его прямо из `text_analyzer`

def test_preprocessor_splits_text():
    text = "Привет, Мир! Как дела?"
    preprocessor = Preprocessor(text)

    assert preprocessor.sentences == ["Привет, Мир!", "Как дела?"]

def test_single_sentence_without_dot():
    preprocessor = Preprocessor("Привет")
    assert preprocessor.sentences == ["Привет"]

def test_preprocessor_handles_multiline_text():
    text = "Привет.\nКак дела?\n\nВсё хорошо!"
    preprocessor = Preprocessor(text)
    assert preprocessor.sentences == ["Привет.", "Как дела?", "Всё хорошо!"]