# Обработка исключений

SchoolMosPy предоставляет иерархию исключений для обработки различных типов ошибок при работе с API.

## Иерархия исключений

```
Exception
└── APIError
    ├── AuthError
    ├── NotFoundError
    ├── ServerError
    └── HTTPError
```

Все исключения находятся в модуле `schoolmospy.utils.exceptions`.

---

## APIError

Базовое исключение для всех ошибок API.

### Определение

```python
class APIError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response: Any | None = None,
    ) -> None:
        ...
```

### Атрибуты

| Атрибут | Тип | Описание |
|---------|-----|----------|
| `message` | `str` | Сообщение об ошибке |
| `status_code` | `int \| None` | HTTP статус код |
| `response` | `Any \| None` | Тело ответа от сервера |

### Использование

```python
from schoolmospy.utils.exceptions import APIError

try:
    marks = await client.marks.get(from_date, to_date)
except APIError as e:
    print(f"Ошибка API: {e}")
    print(f"Статус код: {e.status_code}")
    print(f"Ответ: {e.response}")
```

---

## AuthError

Исключение для ошибок аутентификации (HTTP 401).

### Когда возникает

- Неверный или истекший токен
- Отсутствие прав доступа
- Невалидный profile_id

### Использование

```python
from schoolmospy.utils.exceptions import AuthError

try:
    profile = await client.get_me()
except AuthError:
    print("Ошибка аутентификации. Проверьте токен и profile_id.")
    # Здесь можно реализовать логику обновления токена
```

### Пример обработки

```python
async def safe_request_with_retry():
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return await client.get_me()
        except AuthError:
            if attempt == max_retries - 1:
                print("Не удалось аутентифицироваться после нескольких попыток")
                raise
            print(f"Попытка {attempt + 1} не удалась, повторяем...")
            # Здесь можно обновить токен
            await asyncio.sleep(1)
```

---

## NotFoundError

Исключение для ошибок "не найдено" (HTTP 404).

### Когда возникает

- Запрашиваемый ресурс не существует
- Неверный ID или GUID
- Ресурс был удален

### Использование

```python
from schoolmospy.utils.exceptions import NotFoundError

try:
    events = await client.events.get(
        from_date, to_date, "invalid-guid"
    )
except NotFoundError:
    print("Ресурс не найден. Проверьте корректность GUID.")
```

---

## ServerError

Исключение для ошибок сервера (HTTP 5xx).

### Когда возникает

- Внутренняя ошибка сервера (500)
- Сервис недоступен (503)
- Тайм-аут шлюза (504)

### Использование

```python
from schoolmospy.utils.exceptions import ServerError
import asyncio

async def request_with_retry():
    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            return await client.marks.get(from_date, to_date)
        except ServerError as e:
            if attempt == max_retries - 1:
                print("Сервер недоступен после нескольких попыток")
                raise

            print(f"Ошибка сервера: {e}. Повтор через {retry_delay}с...")
            await asyncio.sleep(retry_delay)
            retry_delay *= 2  # Экспоненциальная задержка
```

---

## HTTPError

Исключение для неожиданных HTTP ошибок.

### Когда возникает

- Любой HTTP статус код, не покрытый другими исключениями
- Неожиданные ошибки клиента (4xx, кроме 401 и 404)

### Использование

```python
from schoolmospy.utils.exceptions import HTTPError

try:
    homeworks = await client.homeworks.get(from_date, to_date)
except HTTPError as e:
    print(f"Неожиданная HTTP ошибка: {e}")
    print(f"Статус: {e.status_code}")
```

---

## Комплексная обработка ошибок

### Обработка всех типов ошибок

```python
from schoolmospy.utils.exceptions import (
    AuthError,
    NotFoundError,
    ServerError,
    HTTPError,
    APIError
)

async def safe_api_call():
    try:
        marks = await client.marks.get(from_date, to_date)
        return marks

    except AuthError:
        print("❌ Ошибка аутентификации")
        print("Проверьте токен и profile_id")

    except NotFoundError:
        print("❌ Ресурс не найден")
        print("Проверьте корректность запроса")

    except ServerError as e:
        print(f"❌ Ошибка сервера: {e.status_code}")
        print("Попробуйте позже")

    except HTTPError as e:
        print(f"❌ HTTP ошибка: {e.status_code}")
        print(f"Детали: {e.response}")

    except APIError as e:
        print(f"❌ Общая ошибка API: {e}")

    return None
```

### Обработка с логированием

```python
import logging

logger = logging.getLogger(__name__)

async def request_with_logging():
    try:
        return await client.get_me()

    except AuthError as e:
        logger.error(f"Auth failed: {e}")
        raise

    except ServerError as e:
        logger.warning(f"Server error: {e.status_code}")
        raise

    except APIError as e:
        logger.error(f"API error: {e}")
        raise
```

### Retry-декоратор

```python
import asyncio
from functools import wraps
from schoolmospy.utils.exceptions import ServerError, APIError

def retry_on_error(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except (ServerError, APIError) as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay * (attempt + 1))
                    continue

            raise last_exception
        return wrapper
    return decorator

@retry_on_error(max_retries=3, delay=2)
async def get_marks_safe():
    return await client.marks.get(from_date, to_date)
```

### Контекстный менеджер для обработки ошибок

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def handle_api_errors():
    try:
        yield
    except AuthError:
        print("Требуется повторная аутентификация")
    except NotFoundError:
        print("Ресурс не найден")
    except ServerError:
        print("Сервер временно недоступен")
    except APIError as e:
        print(f"Ошибка API: {e}")

# Использование
async with handle_api_errors():
    marks = await client.marks.get(from_date, to_date)
```

---

## Лучшие практики

### 1. Специфичная обработка

Обрабатывайте специфичные исключения перед общими:

```python
try:
    result = await client.get_me()
except AuthError:
    # Специфичная обработка
    handle_auth_error()
except APIError:
    # Общая обработка
    handle_generic_error()
```

### 2. Логирование ошибок

Всегда логируйте ошибки для отладки:

```python
import logging

try:
    marks = await client.marks.get(from_date, to_date)
except APIError as e:
    logging.error(f"Failed to get marks: {e}", exc_info=True)
    raise
```

### 3. Graceful degradation

Предоставляйте fallback при ошибках:

```python
async def get_marks_or_empty():
    try:
        return await client.marks.get(from_date, to_date)
    except APIError:
        logging.warning("Failed to get marks, returning empty list")
        return []
```

### 4. Timeout handling

Используйте таймауты для избежания зависания:

```python
import asyncio

try:
    marks = await asyncio.wait_for(
        client.marks.get(from_date, to_date),
        timeout=10.0
    )
except asyncio.TimeoutError:
    print("Запрос превысил таймаут")
except APIError as e:
    print(f"Ошибка API: {e}")
```

## См. также

- [StudentClient](api/student_client.md) - Основной клиент
- [Quick Start](quickstart.md) - Руководство по началу работы
