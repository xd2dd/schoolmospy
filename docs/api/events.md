# EventClient

`EventClient` - клиент для получения расписания и событий ученика за указанный период времени.

## Доступ

Доступ к `EventClient` осуществляется через свойство `events` объекта `StudentClient`:

```python
from schoolmospy import StudentClient

client = StudentClient(token="ваш_токен", profile_id=12345)
event_client = client.events
```

## Методы

### `get()`

Получить события и расписание за указанный период времени.

```python
async def get(
    from_date: datetime,
    to_date: datetime,
    contingent_guid: str
) -> Events
```

#### Параметры

| Параметр | Тип | Описание |
|----------|-----|----------|
| `from_date` | `datetime` | Начальная дата периода (включительно) |
| `to_date` | `datetime` | Конечная дата периода (включительно) |
| `contingent_guid` | `str` | GUID контингента ученика (получается из профиля) |

#### Возвращает

`Events` - модель Pydantic, содержащая список событий и уроков.

#### Исключения

- `APIError` - если запрос не удался или вернул неожиданный ответ
- `AuthError` - если предоставленный токен недействителен или истек

#### Пример

```python
from datetime import datetime
from schoolmospy import StudentClient

async def main():
    client = StudentClient(token="ваш_токен", profile_id=12345)

    # Получение профиля для contingent_guid
    profile = await client.get_me()
    contingent_guid = profile.children[0].contingent_guid

    # Получение расписания на неделю
    events = await client.events.get(
        from_date=datetime(2024, 12, 2),
        to_date=datetime(2024, 12, 8),
        contingent_guid=contingent_guid
    )

    # Обработка событий
    for event in events.response:
        print(f"Предмет: {event.subject_name}")
        print(f"Время: {event.begin_time} - {event.end_time}")
        print(f"Кабинет: {event.room_name}")
        print(f"Учитель: {event.teacher}")
        print("---")
```

## Структура данных Events

Объект `Events` содержит следующие поля:

```python
class Events(BaseModel):
    response: list[Event]  # Список событий
```

### Поля Event

Каждый объект `Event` в списке `response` содержит:

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `int` | Уникальный идентификатор события |
| `subject_name` | `str` | Название предмета |
| `subject_id` | `int` | ID предмета |
| `begin_time` | `str` | Время начала урока |
| `end_time` | `str` | Время окончания урока |
| `date` | `str` | Дата проведения |
| `room_name` | `str \| None` | Название кабинета |
| `room_number` | `str \| None` | Номер кабинета |
| `teacher` | `str \| None` | ФИО учителя |
| `marks` | `list \| None` | Оценки за урок |
| `homework` | `dict \| None` | Домашнее задание |
| `is_cancelled` | `bool` | Отменен ли урок |
| `absence_reason` | `str \| None` | Причина отсутствия |

## Примеры использования

### Получение расписания на сегодня

```python
from datetime import datetime

async def get_today_schedule():
    profile = await client.get_me()
    contingent_guid = profile.children[0].contingent_guid

    today = datetime.now()

    events = await client.events.get(
        from_date=today,
        to_date=today,
        contingent_guid=contingent_guid
    )

    print(f"Уроков сегодня: {len(events.response)}")

    for event in sorted(events.response, key=lambda e: e.begin_time):
        print(f"{event.begin_time} - {event.subject_name} ({event.room_name})")
```

### Получение расписания на неделю

```python
from datetime import datetime, timedelta

async def get_week_schedule():
    profile = await client.get_me()
    contingent_guid = profile.children[0].contingent_guid

    today = datetime.now()
    week_end = today + timedelta(days=7)

    events = await client.events.get(
        from_date=today,
        to_date=week_end,
        contingent_guid=contingent_guid
    )

    # Группировка по дням
    from collections import defaultdict
    by_day = defaultdict(list)

    for event in events.response:
        by_day[event.date].append(event)

    for date, day_events in sorted(by_day.items()):
        print(f"\n=== {date} ===")
        for event in sorted(day_events, key=lambda e: e.begin_time):
            print(f"  {event.begin_time} - {event.subject_name}")
```

### Поиск уроков по предмету

```python
async def find_lessons_by_subject(subject_name: str):
    profile = await client.get_me()
    contingent_guid = profile.children[0].contingent_guid

    events = await client.events.get(
        from_date=datetime(2024, 12, 1),
        to_date=datetime(2024, 12, 31),
        contingent_guid=contingent_guid
    )

    # Фильтрация по предмету
    lessons = [
        e for e in events.response
        if subject_name.lower() in e.subject_name.lower()
    ]

    print(f"Найдено уроков по '{subject_name}': {len(lessons)}")

    for lesson in lessons:
        print(f"{lesson.date} {lesson.begin_time} - {lesson.teacher}")
```

### Проверка домашних заданий в расписании

```python
async def check_homework_in_schedule():
    profile = await client.get_me()
    contingent_guid = profile.children[0].contingent_guid

    today = datetime.now()
    week_end = today + timedelta(days=7)

    events = await client.events.get(
        from_date=today,
        to_date=week_end,
        contingent_guid=contingent_guid
    )

    # Фильтрация уроков с домашним заданием
    with_homework = [
        e for e in events.response
        if e.homework
    ]

    print(f"Уроков с домашним заданием: {len(with_homework)}")

    for event in with_homework:
        print(f"{event.date} - {event.subject_name}")
        print(f"  ДЗ: {event.homework.get('description', 'Нет описания')}")
```

### Поиск отмененных уроков

```python
async def find_cancelled_lessons():
    profile = await client.get_me()
    contingent_guid = profile.children[0].contingent_guid

    events = await client.events.get(
        from_date=datetime(2024, 12, 1),
        to_date=datetime(2024, 12, 31),
        contingent_guid=contingent_guid
    )

    # Фильтрация отмененных уроков
    cancelled = [e for e in events.response if e.is_cancelled]

    print(f"Отмененных уроков: {len(cancelled)}")

    for event in cancelled:
        print(f"{event.date} - {event.subject_name}")
```

### Подсчет статистики по кабинетам

```python
from collections import Counter

async def count_rooms_usage():
    profile = await client.get_me()
    contingent_guid = profile.children[0].contingent_guid

    events = await client.events.get(
        from_date=datetime(2024, 12, 1),
        to_date=datetime(2024, 12, 31),
        contingent_guid=contingent_guid
    )

    # Подсчет использования кабинетов
    rooms = [e.room_name for e in events.response if e.room_name]
    room_counts = Counter(rooms)

    print("Статистика по кабинетам:")
    for room, count in room_counts.most_common():
        print(f"  {room}: {count} уроков")
```

## Обработка ошибок

```python
from schoolmospy.utils.exceptions import AuthError, APIError

async def safe_get_events():
    try:
        profile = await client.get_me()
        contingent_guid = profile.children[0].contingent_guid

        events = await client.events.get(
            from_date=datetime(2024, 12, 1),
            to_date=datetime(2024, 12, 7),
            contingent_guid=contingent_guid
        )
        return events
    except AuthError:
        print("Ошибка аутентификации. Проверьте токен.")
    except APIError as e:
        print(f"Ошибка API: {e}")
    return None
```

## См. также

- [StudentClient](student_client.md) - Основной клиент
- [MarksClient](marks.md) - Получение оценок
- [HomeworkClient](homeworks.md) - Получение домашних заданий
- [Модели](../models.md) - Подробное описание моделей данных
