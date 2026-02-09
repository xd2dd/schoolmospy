# MarksClient

`MarksClient` - клиент для получения оценок ученика за указанный период времени.

## Доступ

Доступ к `MarksClient` осуществляется через свойство `marks` объекта `StudentClient`:

```python
from schoolmospy import StudentClient

client = StudentClient(token="ваш_токен", profile_id=12345)
marks_client = client.marks
```

## Методы

### `get()`

Получить оценки за указанный период времени.

```python
async def get(
    from_date: datetime,
    to_date: datetime
) -> Marks
```

#### Параметры

| Параметр | Тип | Описание |
|----------|-----|----------|
| `from_date` | `datetime` | Начальная дата периода (включительно) |
| `to_date` | `datetime` | Конечная дата периода (включительно) |

#### Возвращает

`Marks` - модель Pydantic, содержащая список оценок.

#### Исключения

- `APIError` - если запрос не удался или вернул неожиданный ответ
- `AuthError` - если предоставленный токен недействителен или истек

#### Пример

```python
from datetime import datetime
from schoolmospy import StudentClient

async def main():
    client = StudentClient(token="ваш_токен", profile_id=12345)

    # Получение оценок за семестр
    marks = await client.marks.get(
        from_date=datetime(2024, 9, 1),
        to_date=datetime(2024, 12, 31)
    )

    # Обработка оценок
    for mark in marks.payload:
        print(f"Предмет: {mark.subject_name}")
        print(f"Оценка: {mark.value}")
        print(f"Дата: {mark.created_at}")
        print(f"Комментарий: {mark.comment}")
        print("---")
```

## Структура данных Marks

Объект `Marks` содержит следующие поля:

```python
class Marks(BaseModel):
    payload: list[Mark]  # Список оценок
```

### Поля Mark

Каждый объект `Mark` в списке `payload` содержит:

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `int` | Уникальный идентификатор оценки |
| `value` | `str` | Значение оценки (например, "5", "4", "зачет") |
| `subject_name` | `str` | Название предмета |
| `subject_id` | `int` | ID предмета |
| `created_at` | `str` | Дата создания оценки |
| `comment` | `str \| None` | Комментарий учителя |
| `is_point` | `bool` | Является ли оценка баллом |
| `point_date` | `str \| None` | Дата контрольной точки |

## Примеры использования

### Получение оценок за текущий месяц

```python
from datetime import datetime

async def get_current_month_marks():
    now = datetime.now()
    start_of_month = datetime(now.year, now.month, 1)

    marks = await client.marks.get(
        from_date=start_of_month,
        to_date=now
    )

    print(f"Оценок за текущий месяц: {len(marks.payload)}")
```

### Фильтрация оценок по предмету

```python
async def get_math_marks():
    marks = await client.marks.get(
        from_date=datetime(2024, 9, 1),
        to_date=datetime(2024, 12, 31)
    )

    # Фильтрация оценок по математике
    math_marks = [
        mark for mark in marks.payload
        if "математик" in mark.subject_name.lower()
    ]

    for mark in math_marks:
        print(f"Математика: {mark.value} - {mark.created_at}")
```

### Подсчет средней оценки

```python
async def calculate_average():
    marks = await client.marks.get(
        from_date=datetime(2024, 9, 1),
        to_date=datetime(2024, 12, 31)
    )

    # Преобразование оценок в числа
    numeric_marks = []
    for mark in marks.payload:
        try:
            numeric_marks.append(int(mark.value))
        except ValueError:
            continue  # Пропускаем не числовые оценки

    if numeric_marks:
        average = sum(numeric_marks) / len(numeric_marks)
        print(f"Средняя оценка: {average:.2f}")
```

### Получение последних оценок

```python
async def get_recent_marks(limit: int = 10):
    marks = await client.marks.get(
        from_date=datetime(2024, 9, 1),
        to_date=datetime.now()
    )

    # Сортировка по дате (новые сначала)
    sorted_marks = sorted(
        marks.payload,
        key=lambda m: m.created_at,
        reverse=True
    )

    # Получение последних N оценок
    recent = sorted_marks[:limit]

    for mark in recent:
        print(f"{mark.created_at}: {mark.subject_name} - {mark.value}")
```

## Обработка ошибок

```python
from schoolmospy.utils.exceptions import AuthError, APIError

async def safe_get_marks():
    try:
        marks = await client.marks.get(
            from_date=datetime(2024, 9, 1),
            to_date=datetime(2024, 12, 31)
        )
        return marks
    except AuthError:
        print("Ошибка аутентификации. Проверьте токен.")
    except APIError as e:
        print(f"Ошибка API: {e}")
    return None
```

## См. также

- [StudentClient](student_client.md) - Основной клиент
- [HomeworkClient](homeworks.md) - Получение домашних заданий
- [EventClient](events.md) - Получение расписания
- [Модели](../models.md) - Подробное описание моделей данных
