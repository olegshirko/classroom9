# Декораторы в Python

> Декоратор — это функция, которая принимает функцию и возвращает новую функцию.

---

## 1. Функции как объекты

В Python функции — полноправные объекты. Их можно передавать, хранить, вызывать динамически.

```python
def greet(name: str) -> str:
    return f"Привет, {name}!"

# Функцию можно присвоить переменной
say_hello = greet
print(say_hello("Иван"))  # Привет, Иван!

# Передать в другую функцию
def run(func, value):
    return func(value)

run(greet, "Мария")  # Привет, Мария!

# Вернуть из функции
def get_greeter():
    def inner(name):
        return f"Привет, {name}!"
    return inner  # возвращаем функцию, не вызываем

greeter = get_greeter()
greeter("Пётр")  # Привет, Пётр!
```

---

## 2. Простой декоратор

Декоратор — функция, которая оборачивает другую функцию.

```python
def my_decorator(func):
    def wrapper():
        print("До вызова")
        func()
        print("После вызова")
    return wrapper

def say_hi():
    print("Привет!")

# Без синтаксиса @
say_hi = my_decorator(say_hi)
say_hi()
# До вызова
# Привет!
# После вызова

# То же самое через @
@my_decorator
def say_hi():
    print("Привет!")

say_hi()
# До вызова
# Привет!
# После вызова
```

`@my_decorator` — это просто сокращение для `say_hi = my_decorator(say_hi)`.

---

## 3. *args и **kwargs — универсальный wrapper

Без них декоратор сломает функции с аргументами.

```python
# ❌ Проблема — wrapper не принимает аргументы
def logger(func):
    def wrapper():
        print(f"Вызов {func.__name__}")
        func()  # а если func принимает аргументы?
    return wrapper

@logger
def add(a, b):
    return a + b

add(1, 2)  # TypeError!

# ✅ Решение — пробрасываем все аргументы
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Вызов {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Результат: {result}")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

add(1, 2)
# Вызов add
# Результат: 3
```

---

## 4. functools.wraps

Без `wraps` декоратор "скрывает" оригинальную функцию.

```python
def logger(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@logger
def add(a, b):
    """Складывает два числа"""
    return a + b

print(add.__name__)  # wrapper  ← неправильно!
print(add.__doc__)   # None     ← документация потерялась!

# ✅ functools.wraps сохраняет метаданные оригинала
from functools import wraps

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@logger
def add(a, b):
    """Складывает два числа"""
    return a + b

print(add.__name__)  # add     ✅
print(add.__doc__)   # Складывает два числа  ✅
```

---

## 5. Декоратор с аргументами

Нужна ещё одна обёртка — фабрика декораторов.

```python
from functools import wraps

def repeat(times: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say(message: str):
    print(message)

say("Привет!")
# Привет!
# Привет!
# Привет!
```

`@repeat(3)` → сначала вызывается `repeat(3)`, возвращает `decorator`, потом `decorator(say)`.

---

## 6. Стек декораторов

Декораторы применяются снизу вверх.

```python
from functools import wraps

def bold(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"**{func(*args, **kwargs)}**"
    return wrapper

def upper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

@bold       # применяется вторым
@upper      # применяется первым
def greet(name: str) -> str:
    return f"привет, {name}"

greet("иван")  # **ПРИВЕТ, ИВАН**

# Эквивалентно:
# greet = bold(upper(greet))
```

---

## 7. Декораторы в FastAPI

`@app.get`, `@app.post` — это декораторы с аргументами. FastAPI регистрирует функцию как обработчик маршрута.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# @app.get("/items") регистрирует функцию get_items
# как обработчик GET-запроса на /items
@app.get("/items")
def get_items():
    return [{"id": 1, "name": "яблоко"}]

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"id": item_id}

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
def create_item(item: Item):
    return {"created": item.name}
```

Свой декоратор для FastAPI — например, логирование:

```python
from functools import wraps
import time

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} выполнялась {elapsed:.3f}с")
        return result
    return wrapper

@app.get("/slow")
@timed
def slow_endpoint():
    time.sleep(0.1)
    return {"status": "ok"}
```

---

## Шпаргалка

```python
# Простой декоратор
def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # до
        result = func(*args, **kwargs)
        # после
        return result
    return wrapper

# Декоратор с аргументами
def decorator(param):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return inner

# Применение
@decorator
def my_func(): ...

@decorator(param=value)
def my_func(): ...
```
