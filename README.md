# Text Analyzer API

REST API-сервис для анализа текста. Принимает текст и возвращает количество слов, символов и топ-5 слов по частоте.

## Запуск

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Swagger UI будет доступен по адресу: http://localhost:8000/docs

## Примеры запросов

### Анализ текста

```bash
curl -X POST "http://localhost:8000/text/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Привет мир! Привет всем!"}'
```

**Ответ:**

```json
{
  "word_count": 4,
  "char_count": 26,
  "char_count_no_spaces": 22,
  "top_words": [
    ["привет", 2],
    ["мир", 1],
    ["всем", 1]
  ]
}
```

### Корневой эндпоинт

```bash
curl http://localhost:8000/
```

**Ответ:**

```json
{
  "message": "Добро пожаловать в Text Analyzer API",
  "docs": "/docs"
}
```

## Структура проекта

```
.
├── main.py          # Точка входа
├── router.py        # Эндпоинты
├── schemas.py       # Pydantic-модели
├── service.py       # Бизнес-логика
├── requirements.txt # Зависимости
└── README.md        # Описание
```
