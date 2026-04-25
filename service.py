import re
from collections import Counter


def analyze_text(text: str) -> dict:
    """Анализирует текст и возвращает статистику."""
    # Извлекаем слова (буквы, цифры, подчёркивания)
    words = re.findall(r"\b\w+\b", text.lower())
    word_count = len(words)
    char_count = len(text)
    char_count_no_spaces = len(text.replace(" ", "").replace("\n", "").replace("\t", ""))
    top_words = Counter(words).most_common(5)

    return {
        "word_count": word_count,
        "char_count": char_count,
        "char_count_no_spaces": char_count_no_spaces,
        "top_words": top_words,
    }
