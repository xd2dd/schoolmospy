# Быстрый старт

Это руководство поможет вам начать работу с SchoolMosPy всего за несколько минут.

## Установка

Установите библиотеку с помощью pip:

```bash
pip install schoolmospy
```

## Аутентификация

Для использования SchoolMosPy вам понадобится:

1. **Token** - токен аутентификации от school.mos.ru
2. **Profile ID** - ID вашего профиля ученика

!!! info "Получение учетных данных"
    Вы можете получить токен и profile_id, изучив сетевые запросы в браузере при входе на school.mos.ru.

## Базовое использование

### Инициализация клиента

```python
from schoolmospy import StudentClient

client = StudentClient(
    token="ваш_токен_здесь",
    profile_id=12345678
)
```

### Получение информации о профиле

Получите информацию о профиле ученика:

```python
import asyncio

async def main():
    profile = await client.get_me()

    # Доступ к данным профиля
    print(f"Имя: {profile.profile.first_name} {profile.profile.last_name}")
    print(f"Email: {profile.profile.email}")

    # Доступ к данным детей (для родительских аккаунтов)
    for child in profile.children:
        print(f"Ребенок: {child.first_name} {child.last_name}")
        print(f"Школа: {child.school.name}")
        print(f"Класс: {child.class_name}")

asyncio.run(main())
```

### Получение оценок

Получите оценки ученика за определенный период:

```python
from datetime import datetime

async def get_marks():
    marks = await client.marks.get(
        from_date=datetime(2024, 9, 1),
        to_date=datetime(2024, 12, 31)
    )

    for mark in marks.payload:
        print(f"Предмет: {mark.subject_name}")
        print(f"Оценка: {mark.value}")
        print(f"Дата: {mark.created_at}")
        print("---")

asyncio.run(get_marks())
```

### Получение домашних заданий

Получите домашние задания:

```python
async def get_homeworks():
    homeworks = await client.homeworks.get(
        from_date=datetime(2024, 9, 1),
        to_date=datetime(2024, 12, 31)
    )

    for hw in homeworks.payload:
        print(f"Предмет: {hw.subject_name}")
        print(f"Описание: {hw.description}")
        print(f"Срок сдачи: {hw.date}")
        print("---")

asyncio.run(get_homeworks())
```

### Получение расписания/событий

Получите расписание и события:

```python
async def get_schedule():
    profile = await client.get_me()
    contingent_guid = profile.children[0].contingent_guid

    events = await client.events.get(
        from_date=datetime(2024, 12, 1),
        to_date=datetime(2024, 12, 7),
        contingent_guid=contingent_guid
    )

    for event in events.response:
        print(f"Предмет: {event.subject_name}")
        print(f"Время: {event.begin_time} - {event.end_time}")
        print(f"Кабинет: {event.room_name}")
        print("---")

asyncio.run(get_schedule())
```

## Полный пример

Вот полный пример, демонстрирующий все основные возможности:

```python
import asyncio
from datetime import datetime
from schoolmospy import StudentClient

async def main():
    # Инициализация клиента
    client = StudentClient(
        token="ваш_токен_здесь",
        profile_id=12345678
    )

    try:
        # Получение профиля
        print("=== Информация о профиле ===")
        profile = await client.get_me()
        print(f"Ученик: {profile.profile.first_name} {profile.profile.last_name}")

        # Получение оценок
        print("\n=== Последние оценки ===")
        marks = await client.marks.get(
            from_date=datetime(2024, 9, 1),
            to_date=datetime(2024, 12, 31)
        )
        print(f"Всего оценок: {len(marks.payload)}")

        # Получение домашних заданий
        print("\n=== Текущие домашние задания ===")
        homeworks = await client.homeworks.get(
            from_date=datetime(2024, 12, 1),
            to_date=datetime(2024, 12, 31)
        )
        print(f"Всего заданий: {len(homeworks.payload)}")

        # Получение расписания
        print("\n=== Расписание на эту неделю ===")
        contingent_guid = profile.children[0].contingent_guid
        events = await client.events.get(
            from_date=datetime(2024, 12, 1),
            to_date=datetime(2024, 12, 7),
            contingent_guid=contingent_guid
        )
        print(f"Всего событий: {len(events.response)}")

    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Обработка ошибок

SchoolMosPy предоставляет специальные исключения для различных типов ошибок:

```python
from schoolmospy.utils.exceptions import AuthError, NotFoundError, ServerError, APIError

async def safe_request():
    try:
        marks = await client.marks.get(
            from_date=datetime(2024, 9, 1),
            to_date=datetime(2024, 12, 31)
        )
    except AuthError:
        print("Ошибка аутентификации. Проверьте токен.")
    except NotFoundError:
        print("Ресурс не найден.")
    except ServerError:
        print("Ошибка сервера. Попробуйте позже.")
    except APIError as e:
        print(f"Ошибка API: {e}")
```

## Следующие шаги

- Изучите [документацию API](api/student_client.md) для подробной информации
- Ознакомьтесь с документацией [Моделей](models.md) для понимания структур данных
- Узнайте об [обработке исключений](exceptions.md)

## Советы

!!! tip "Производительность"
    Используйте asyncio для выполнения параллельных запросов для лучшей производительности:
    ```python
    marks, homeworks = await asyncio.gather(
        client.marks.get(from_date, to_date),
        client.homeworks.get(from_date, to_date)
    )
    ```

!!! warning "Ограничение скорости"
    Помните об ограничениях скорости при выполнении запросов к API. Реализуйте соответствующие задержки при необходимости.

!!! note "Истечение токена"
    Токены могут истекать. Реализуйте логику обновления токена в продакшен приложениях.
