# HomeworkClient

`HomeworkClient` - клиент для получения домашних заданий ученика за указанный период времени.

## Доступ

Доступ к `HomeworkClient` осуществляется через свойство `homeworks` объекта `StudentClient`:

```python
from schoolmospy import StudentClient

client = StudentClient(token="ваш_токен", profile_id=12345)
homework_client = client.homeworks
```

## Методы

### `get()`

Получить домашние задания за указанный период времени.

```python
async def get(
    from_date: datetime,
    to_date: datetime
) -> Homeworks
```

#### Параметры

| Параметр | Тип | Описание |
|----------|-----|----------|
| `from_date` | `datetime` | Начальная дата периода (включительно) |
| `to_date` | `datetime` | Конечная дата периода (включительно) |

#### Возвращает

`Homeworks` - модель Pydantic, содержащая список домашних заданий.

#### Исключения

- `APIError` - если запрос не удался или вернул неожиданный ответ
- `AuthError` - если предоставленный токен недействителен или истек

#### Пример

```python
from datetime import datetime
from schoolmospy import StudentClient

async def main():
    client = StudentClient(token="ваш_токен", profile_id=12345)

    # Получение домашних заданий за месяц
    homeworks = await client.homeworks.get(
        from_date=datetime(2024, 12, 1),
        to_date=datetime(2024, 12, 31)
    )

    # Обработка домашних заданий
    for hw in homeworks.payload:
        print(f"Предмет: {hw.subject_name}")
        print(f"Описание: {hw.description}")
        print(f"Срок сдачи: {hw.date}")
        print(f"Прикрепленные файлы: {len(hw.attachments) if hw.attachments else 0}")
        print("---")
```

### `done()`

Отметить домашнее задание как выполненное.

```python
async def done(
    homework_id: int
) -> DoneStatus
```

#### Параметры

| Параметр | Тип | Описание |
|----------|-----|----------|
| `homework_id` | `int` | Уникальный идентификатор домашнего задания |

!!! info "Использование ID домашнего задания"
    В качестве ID следует использовать поле `homework_entry_student_id` в типе `Homework`

#### Возвращает

`DoneStatus` - модель, содержащая статус выполнения операции.

```python
class DoneStatus(BaseModel):
    success: bool  # True, если задание успешно отмечено как выполненное
```

#### Исключения

- `APIError` - если запрос не удался или вернул неожиданный ответ
- `AuthError` - если предоставленный токен недействителен или истек
- `NotFoundError` - если домашнее задание с указанным ID не найдено

#### Пример

```python
from schoolmospy import StudentClient

async def main():
    client = StudentClient(token="ваш_токен", profile_id=12345)

    # Отметка задания как выполненного
    result = await client.homeworks.done(homework_id=123456)

    if result.success:
        print("✓ Задание отмечено как выполненное")
    else:
        print("✗ Не удалось отметить задание")
```

#### Пример с получением и отметкой заданий

```python
from datetime import datetime

async def mark_homeworks_done():
    client = StudentClient(token="ваш_токен", profile_id=12345)

    # Получаем задания за текущую неделю
    homeworks = await client.homeworks.get(
        from_date=datetime(2024, 12, 1),
        to_date=datetime(2024, 12, 7)
    )

    # Отмечаем невыполненные задания как выполненные
    for hw in homeworks.payload:
        if not hw.is_done:
            result = await client.homeworks.done(homework_id=hw.homework_entry_student_id)
            if result.success:
                print(f"✓ {hw.subject_name}: задание выполнено")
```

## Структура данных Homeworks

Объект `Homeworks` содержит следующие поля:

```python
class Homeworks(BaseModel):
    payload: list[Homework]  # Список домашних заданий
```

### Поля Homework

Каждый объект `Homework` в списке `payload` содержит:

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `int` | Уникальный идентификатор задания |
| `subject_name` | `str` | Название предмета |
| `subject_id` | `int` | ID предмета |
| `description` | `str` | Описание задания |
| `date` | `str` | Дата выдачи/срок сдачи |
| `homework_entry_student_id` | `int \| None` | ID записи студента |
| `is_done` | `bool` | Выполнено ли задание |
| `attachments` | `list \| None` | Список прикрепленных файлов |
| `additional_materials` | `list \| None` | Дополнительные материалы |

## Примеры использования

### Получение текущих домашних заданий

```python
from datetime import datetime, timedelta

async def get_current_homeworks():
    today = datetime.now()
    next_week = today + timedelta(days=7)

    homeworks = await client.homeworks.get(
        from_date=today,
        to_date=next_week
    )

    print(f"Заданий на ближайшую неделю: {len(homeworks.payload)}")

    for hw in homeworks.payload:
        status = "✓ Выполнено" if hw.is_done else "✗ Не выполнено"
        print(f"{hw.subject_name} - {status}")
```

### Фильтрация невыполненных заданий

```python
async def get_pending_homeworks():
    homeworks = await client.homeworks.get(
        from_date=datetime(2024, 12, 1),
        to_date=datetime(2024, 12, 31)
    )

    # Фильтрация невыполненных заданий
    pending = [hw for hw in homeworks.payload if not hw.is_done]

    print(f"Невыполненных заданий: {len(pending)}")

    for hw in pending:
        print(f"⚠️ {hw.subject_name}: {hw.description[:50]}...")
```

### Группировка заданий по предметам

```python
from collections import defaultdict

async def group_homeworks_by_subject():
    homeworks = await client.homeworks.get(
        from_date=datetime(2024, 12, 1),
        to_date=datetime(2024, 12, 31)
    )

    # Группировка по предметам
    by_subject = defaultdict(list)
    for hw in homeworks.payload:
        by_subject[hw.subject_name].append(hw)

    # Вывод статистики
    for subject, tasks in by_subject.items():
        done = sum(1 for t in tasks if t.is_done)
        total = len(tasks)
        print(f"{subject}: {done}/{total} выполнено")
```

### Поиск заданий с прикрепленными файлами

```python
async def find_homeworks_with_attachments():
    homeworks = await client.homeworks.get(
        from_date=datetime(2024, 9, 1),
        to_date=datetime(2024, 12, 31)
    )

    # Фильтрация заданий с вложениями
    with_files = [
        hw for hw in homeworks.payload
        if hw.attachments and len(hw.attachments) > 0
    ]

    for hw in with_files:
        print(f"{hw.subject_name}: {len(hw.attachments)} файлов")
        for attachment in hw.attachments:
            print(f"  - {attachment.get('name', 'Без названия')}")
```

### Подсчет статистики выполнения

```python
async def calculate_completion_rate():
    homeworks = await client.homeworks.get(
        from_date=datetime(2024, 9, 1),
        to_date=datetime(2024, 12, 31)
    )

    total = len(homeworks.payload)
    done = sum(1 for hw in homeworks.payload if hw.is_done)

    if total > 0:
        rate = (done / total) * 100
        print(f"Выполнено: {done} из {total} ({rate:.1f}%)")
```

## Обработка ошибок

```python
from schoolmospy.utils.exceptions import AuthError, APIError

async def safe_get_homeworks():
    try:
        homeworks = await client.homeworks.get(
            from_date=datetime(2024, 12, 1),
            to_date=datetime(2024, 12, 31)
        )
        return homeworks
    except AuthError:
        print("Ошибка аутентификации. Проверьте токен.")
    except APIError as e:
        print(f"Ошибка API: {e}")
    return None
```

## См. также

- [StudentClient](student_client.md) - Основной клиент
- [MarksClient](marks.md) - Получение оценок
- [EventClient](events.md) - Получение расписания
- [Модели](../models.md) - Подробное описание моделей данных
