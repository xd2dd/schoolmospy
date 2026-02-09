# StudentClient

`StudentClient` - это основной клиентский класс для взаимодействия с API school.mos.ru. Он предоставляет доступ ко всем функциям, связанным с учеником.

## Определение класса

```python
from schoolmospy import StudentClient
```

## Конструктор

```python
StudentClient(
    base_url: str = "https://school.mos.ru",
    token: str | None = None,
    profile_id: int | None = None,
    profile_type: str = "student",
    timeout: float = 15.0
)
```

### Параметры

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| `base_url` | `str` | `"https://school.mos.ru"` | Базовый URL для API |
| `token` | `str \| None` | `None` | Токен аутентификации |
| `profile_id` | `int \| None` | `None` | ID профиля ученика |
| `profile_type` | `str` | `"student"` | Тип профиля (student/parent) |
| `timeout` | `float` | `15.0` | Таймаут запроса в секундах |

### Пример

```python
from schoolmospy import StudentClient

client = StudentClient(
    token="ваш_токен",
    profile_id=12345678
)
```

## Свойства

### `marks`

Доступ к MarksClient для получения оценок ученика.

**Тип:** `MarksClient`

```python
marks = await client.marks.get(from_date, to_date)
```

### `homeworks`

Доступ к HomeworkClient для получения домашних заданий.

**Тип:** `HomeworkClient`

```python
homeworks = await client.homeworks.get(from_date, to_date)
```

### `events`

Доступ к EventClient для получения расписания и событий.

**Тип:** `EventClient`

```python
events = await client.events.get(from_date, to_date, contingent_guid)
```

## Методы

### `get_me()`

Получить информацию о профиле текущего пользователя.

**Возвращает:** `Profile` - объект профиля, содержащий данные пользователя

**Исключения:**
- `APIError` - если запрос не удался
- `AuthError` - если аутентификация не прошла

**Пример:**

```python
profile = await client.get_me()

print(f"Имя: {profile.profile.first_name} {profile.profile.last_name}")
print(f"Email: {profile.profile.email}")
print(f"Телефон: {profile.profile.phone}")

# Доступ к данным детей
for child in profile.children:
    print(f"Ребенок: {child.first_name} {child.last_name}")
    print(f"Школа: {child.school.name}")
    print(f"Класс: {child.class_name}")
```

**Структура ответа:**

```python
{
    "profile": {
        "first_name": "Иван",
        "last_name": "Иванов",
        "middle_name": "Иванович",
        "email": "example@example.com",
        "phone": "+79991234567",
        ...
    },
    "children": [
        {
            "first_name": "...",
            "last_name": "...",
            "school": {...},
            "class_name": "11-А",
            "contingent_guid": "...",
            ...
        }
    ]
}
```

---

### `userinfo()`

Получить базовую информацию о пользователе из OAuth.

**Возвращает:** `Userinfo` - объект с базовой информацией о пользователе

**Исключения:**
- `APIError` - если запрос не удался
- `AuthError` - если аутентификация не прошла

**Пример:**

```python
userinfo = await client.userinfo()

print(f"ID пользователя: {userinfo.user_id}")
print(f"Имя: {userinfo.name}")
```

## Полный пример

```python
import asyncio
from datetime import datetime
from schoolmospy import StudentClient

async def main():
    # Инициализация клиента
    client = StudentClient(
        token="ваш_токен",
        profile_id=12345678
    )

    # Получение профиля
    profile = await client.get_me()
    print(f"Ученик: {profile.profile.first_name} {profile.profile.last_name}")

    # Получение оценок за текущий семестр
    marks = await client.marks.get(
        from_date=datetime(2024, 9, 1),
        to_date=datetime(2024, 12, 31)
    )
    print(f"Всего оценок: {len(marks.payload)}")

    # Получение домашних заданий
    homeworks = await client.homeworks.get(
        from_date=datetime(2024, 12, 1),
        to_date=datetime(2024, 12, 31)
    )
    print(f"Всего заданий: {len(homeworks.payload)}")

    # Получение расписания
    contingent_guid = profile.children[0].contingent_guid
    events = await client.events.get(
        from_date=datetime(2024, 12, 1),
        to_date=datetime(2024, 12, 7),
        contingent_guid=contingent_guid
    )
    print(f"Всего событий: {len(events.response)}")

asyncio.run(main())
```

## Обработка ошибок

```python
from schoolmospy.utils.exceptions import AuthError, APIError

async def safe_example():
    try:
        client = StudentClient(
            token="ваш_токен",
            profile_id=12345
        )
        profile = await client.get_me()
    except AuthError:
        print("Ошибка аутентификации")
    except APIError as e:
        print(f"Ошибка API: {e}")
```

## См. также

- [MarksClient](marks.md) - Получение оценок ученика
- [HomeworkClient](homeworks.md) - Получение домашних заданий
- [EventClient](events.md) - Доступ к расписанию и событиям
- [Модели](../models.md) - Справочник моделей данных
- [Исключения](../exceptions.md) - Обработка ошибок
