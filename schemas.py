from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Текст для анализа")


class TextAnalysisResponse(BaseModel):
    word_count: int = Field(..., description="Количество слов")
    char_count: int = Field(..., description="Количество символов (с пробелами)")
    char_count_no_spaces: int = Field(..., description="Количество символов (без пробелов)")
    top_words: list[tuple[str, int]] = Field(..., description="Топ-5 слов по частоте")
