# Pythonic Way — как писать код по-питоновски

> "Code is read much more often than it is written." — Guido van Rossum

---

## 1. List / Dict / Set Comprehensions

Вместо цикла с `append` — одно выражение.

```python
# ❌ Не питонично
squares = []
for x in range(10):
    if x % 2 == 0:
        squares.append(x ** 2)

# ✅ Питонично
squares = [x ** 2 for x in range(10) if x % 2 == 0]
```

```python
# Dict comprehension
words = ["hello", "world", "python"]
lengths = {word: len(word) for word in words}
# {"hello": 5, "world": 5, "python": 6}

# Set comprehension — уникальные значения
unique_lengths = {len(word) for word in words}
# {5, 6}
```

---

## 2. Unpacking

Python умеет распаковывать последовательности прямо в переменные.

```python
# Простой swap без temp
a, b = 1, 2
a, b = b, a

# Распаковка кортежа/списка
first, second, third = [10, 20, 30]

# Сбор остатка через *
first, *rest = [1, 2, 3, 4, 5]
# first = 1, rest = [2, 3, 4, 5]

*init, last = [1, 2, 3, 4, 5]
# init = [1, 2, 3, 4], last = 5

# Распаковка словаря при вызове функции
def greet(name, age):
    return f"Привет, {name}! Тебе {age} лет."

data = {"name": "Иван", "age": 20}
greet(**data)  # Привет, Иван! Тебе 20 лет.
```

---

## 3. f-strings

Самый читаемый и быстрый способ форматировать строки.

```python
name = "Анна"
score = 95.678

# ❌ Конкатенация — неудобно
result = "Студент " + name + " набрал " + str(score) + " баллов"

# ❌ .format() — многословно
result = "Студент {} набрал {} баллов".format(name, score)

# ✅ f-string
result = f"Студент {name} набрал {score} баллов"

# Форматирование числа прямо внутри
result = f"Студент {name} набрал {score:.1f} баллов"  # 95.7

# Выражения внутри {}
result = f"2 + 2 = {2 + 2}"
result = f"Имя в верхнем регистре: {name.upper()}"
```

---

## 4. enumerate и zip

Никогда не пишите `range(len(...))`.

```python
fruits = ["яблоко", "банан", "груша"]

# ❌ Антипаттерн
for i in range(len(fruits)):
    print(i, fruits[i])

# ✅ enumerate — индекс + значение
for i, fruit in enumerate(fruits):
    print(i, fruit)

# Начать счёт не с 0
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")
```

```python
names = ["Иван", "Мария", "Пётр"]
scores = [85, 92, 78]

# ❌ Антипаттерн
for i in range(len(names)):
    print(names[i], scores[i])

# ✅ zip — итерация по двум спискам одновременно
for name, score in zip(names, scores):
    print(f"{name}: {score}")
```

---

## 5. Контекстные менеджеры (with)

`with` гарантирует, что ресурс будет закрыт даже при ошибке.

```python
# ❌ Опасно — если возникнет исключение, файл не закроется
f = open("data.txt", "r")
content = f.read()
f.close()

# ✅ with автоматически закрывает файл
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Несколько ресурсов сразу
with open("input.txt") as fin, open("output.txt", "w") as fout:
    fout.write(fin.read())
```

---

## 6. Именованные аргументы и дефолты

Функции должны быть читаемы без заглядывания в документацию.

```python
# ❌ Что означают True и 8?
generate_password(True, False, 8)

# ✅ Сразу понятно
generate_password(use_digits=True, use_symbols=False, length=8)

# Дефолтные значения — делают аргументы необязательными
def generate_password(length: int = 12, use_digits: bool = True, use_symbols: bool = False):
    ...

generate_password()                  # все дефолты
generate_password(length=20)         # только длина
generate_password(20, use_symbols=True)
```

---

## 7. Type Hints

Аннотации типов делают код понятнее и помогают IDE находить ошибки. В FastAPI — обязательны.

```python
# Без аннотаций — непонятно что принимает и возвращает функция
def process(data, limit):
    ...

# ✅ С аннотациями
def process(data: str, limit: int = 10) -> list[str]:
    ...
```

```python
from typing import Optional

# Optional — значение может быть None
def find_user(user_id: int) -> Optional[dict]:
    ...

# В FastAPI это используется повсюду
from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str
    max_words: int = 100
    language: Optional[str] = None
```

---

## 8. Соглашения по именованию

```python
# Обычная переменная / функция — snake_case
user_name = "Иван"
def get_user_by_id(user_id: int): ...

# Класс — PascalCase
class UserService: ...

# Константа — UPPER_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# "Приватное" — одно подчёркивание (соглашение, не запрет)
def _internal_helper(): ...

# Игнорируемая переменная
for _ in range(5):
    print("привет")

# Конфликт с ключевым словом
type_ = "admin"   # не type, потому что type — встроенная функция
```

---

## 9. Исключения

Ловите конкретные исключения, а не всё подряд.

```python
# ❌ Плохо — скрывает все ошибки, включая баги
try:
    result = int(user_input)
except:
    print("Ошибка")

# ❌ Тоже плохо
try:
    result = int(user_input)
except Exception:
    print("Ошибка")

# ✅ Конкретный тип
try:
    result = int(user_input)
except ValueError:
    print("Введите целое число")

# Несколько типов
try:
    data = json.loads(text)
    value = data["key"]
except json.JSONDecodeError:
    print("Невалидный JSON")
except KeyError:
    print("Ключ не найден")

# В FastAPI — HTTPException вместо return с ошибкой
from fastapi import HTTPException

def get_item(item_id: int):
    if item_id < 0:
        raise HTTPException(status_code=400, detail="ID должен быть положительным")
```

---

## Быстрая шпаргалка

| Антипаттерн | Питонично |
|---|---|
| `for i in range(len(x))` | `for i, v in enumerate(x)` |
| `x = []; for ... x.append(v)` | `x = [v for ...]` |
| `"Hello " + name` | `f"Hello {name}"` |
| `except:` | `except ValueError:` |
| `f.open(); ...; f.close()` | `with open(...) as f:` |
| `def fn(a, b, c): fn(1, True, 8)` | именованные аргументы |
