# LessonScheduleClient

`LessonScheduleClient` - клиент для получения детальной информации по конкретному уроку.

## Доступ

Доступ к `LessonScheduleClient` осуществляется через свойство `lesson_schedule` объекта `StudentClient`:

```python
from schoolmospy import StudentClient

client = StudentClient(token="ваш_токен", profile_id=12345)
lesson_client = client.lesson_schedule
```

## Методы

### `get_item()`

Получить детальную информацию об уроке по ID элемента расписания.

```python
async def get_item(
    item_id: int,
    person_id: str,
    student_id: int | None = None,
    lesson_type: str = "PLAN",
    row_limit: int = 54
) -> LessonScheduleItem
```

#### Параметры

| Параметр | Тип | Описание |
|----------|-----|----------|
| `item_id` | `int` | ID элемента расписания |
| `person_id` | `str` | GUID ученика (`contingent_guid`) |
| `student_id` | `int \| None` | ID профиля ученика, по умолчанию `profile_id` клиента |
| `lesson_type` | `str` | Тип урока (например, `PLAN`) |
| `row_limit` | `int` | Ограничение количества строк ответа |

#### Возвращает

`LessonScheduleItem` - модель Pydantic с полной информацией об уроке.

#### Пример

```python
lesson = await client.lesson_schedule.get_item(
    item_id=594787540,
    person_id=profile.children[0].contingent_guid,
)

print(lesson.subject_name, lesson.begin_time, lesson.end_time)
for hw in lesson.lesson_homeworks:
    print(hw.homework)
```

## См. также

- [StudentClient](student_client.md) - Основной клиент
- [EventClient](events.md) - Список событий и уроков
- [Модели](../models.md) - Подробное описание моделей данных
