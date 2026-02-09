# Модели данных

SchoolMosPy использует Pydantic для валидации и типизации данных. Все модели данных являются наследниками `BaseModel` из Pydantic.

## Profile

Модель профиля пользователя, содержащая информацию об учетной записи и детях.

### Структура

```python
class Profile(BaseModel):
    profile: _Profile  # Основная информация профиля
    children: list[Child]  # Список детей
    hash: str  # Хэш профиля
```

### _Profile (Основной профиль)

| Поле | Тип | Описание |
|------|-----|----------|
| `last_name` | `str` | Фамилия |
| `first_name` | `str` | Имя |
| `middle_name` | `str` | Отчество |
| `birth_date` | `str` | Дата рождения |
| `sex` | `str` | Пол |
| `user_id` | `int` | ID пользователя |
| `id` | `int` | ID профиля |
| `phone` | `str` | Телефон |
| `email` | `str` | Email |
| `snils` | `str` | СНИЛС |
| `type` | `str` | Тип профиля |

### Child (Ребенок)

| Поле | Тип | Описание |
|------|-----|----------|
| `last_name` | `str` | Фамилия |
| `first_name` | `str` | Имя |
| `middle_name` | `str` | Отчество |
| `birth_date` | `str` | Дата рождения |
| `sex` | `str` | Пол |
| `user_id` | `int` | ID пользователя |
| `id` | `int` | ID ребенка |
| `phone` | `str` | Телефон |
| `email` | `str` | Email |
| `snils` | `str` | СНИЛС |
| `school` | `School` | Информация о школе |
| `class_name` | `str` | Название класса |
| `class_level_id` | `int` | ID уровня класса |
| `class_unit_id` | `int` | ID класса |
| `class_uid` | `str` | UID класса |
| `age` | `int` | Возраст |
| `groups` | `list[Group]` | Список групп |
| `representatives` | `list[Representative]` | Список представителей |
| `sections` | `list[Section]` | Список секций |
| `contingent_guid` | `str` | GUID контингента (используется для запросов) |
| `enrollment_date` | `str` | Дата зачисления |

### School (Школа)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `int` | ID школы |
| `name` | `str` | Полное название школы |
| `short_name` | `str` | Короткое название |
| `county` | `str` | Округ |
| `principal` | `str` | ФИО директора |
| `phone` | `str` | Телефон школы |
| `global_school_id` | `int` | Глобальный ID школы |

### Пример использования

```python
profile = await client.get_me()

# Доступ к основному профилю
print(f"Имя: {profile.profile.first_name}")
print(f"Email: {profile.profile.email}")

# Доступ к данным ребенка
child = profile.children[0]
print(f"Ребенок: {child.first_name} {child.last_name}")
print(f"Школа: {child.school.name}")
print(f"Класс: {child.class_name}")

# Получение contingent_guid для запросов
contingent_guid = child.contingent_guid
```

---

## Marks

Модель оценок ученика.

### Структура

```python
class Marks(BaseModel):
    payload: list[Mark]  # Список оценок
```

### Mark (Оценка)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `int` | ID оценки |
| `value` | `str` | Значение оценки ("5", "4", "зачет" и т.д.) |
| `subject_name` | `str` | Название предмета |
| `subject_id` | `int` | ID предмета |
| `created_at` | `str` | Дата создания |
| `updated_at` | `str` | Дата обновления |
| `comment` | `str \| None` | Комментарий учителя |
| `control_form_name` | `str \| None` | Форма контроля |
| `is_point` | `bool` | Является ли контрольной точкой |
| `point_date` | `str \| None` | Дата контрольной точки |
| `weight` | `int \| None` | Вес оценки |

### Пример использования

```python
marks = await client.marks.get(from_date, to_date)

for mark in marks.payload:
    print(f"{mark.subject_name}: {mark.value}")
    if mark.comment:
        print(f"  Комментарий: {mark.comment}")
```

---

## Homeworks

Модель домашних заданий.

### Структура

```python
class Homeworks(BaseModel):
    payload: list[Homework]  # Список домашних заданий
```

### Homework (Домашнее задание)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `int` | ID задания |
| `subject_name` | `str` | Название предмета |
| `subject_id` | `int` | ID предмета |
| `description` | `str` | Описание задания |
| `date` | `str` | Дата задания |
| `date_assigned` | `str` | Дата выдачи |
| `homework_entry_student_id` | `int \| None` | ID записи студента |
| `is_done` | `bool` | Выполнено ли |
| `attachments` | `list \| None` | Прикрепленные файлы |
| `additional_materials` | `list \| None` | Дополнительные материалы |

### Пример использования

```python
homeworks = await client.homeworks.get(from_date, to_date)

for hw in homeworks.payload:
    status = "✓" if hw.is_done else "✗"
    print(f"{status} {hw.subject_name}: {hw.description}")

    if hw.attachments:
        print(f"  Файлов: {len(hw.attachments)}")
```

---

## Events

Модель событий и расписания.

### Структура

```python
class Events(BaseModel):
    response: list[Event]  # Список событий
```

### Event (Событие/Урок)

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | `int` | ID события |
| `subject_name` | `str` | Название предмета |
| `subject_id` | `int` | ID предмета |
| `begin_time` | `str` | Время начала |
| `end_time` | `str` | Время окончания |
| `date` | `str` | Дата проведения |
| `room_name` | `str \| None` | Название кабинета |
| `room_number` | `str \| None` | Номер кабинета |
| `building_name` | `str \| None` | Название здания |
| `teacher` | `str \| None` | ФИО учителя |
| `lesson_type` | `str \| None` | Тип урока |
| `marks` | `list \| None` | Оценки за урок |
| `homework` | `dict \| None` | Домашнее задание |
| `is_cancelled` | `bool` | Отменен ли урок |
| `absence_reason` | `str \| None` | Причина отсутствия |
| `non_attendance_reason` | `str \| None` | Причина неявки |

### Пример использования

```python
events = await client.events.get(from_date, to_date, contingent_guid)

for event in events.response:
    print(f"{event.begin_time}-{event.end_time}: {event.subject_name}")
    print(f"  Кабинет: {event.room_name}")
    print(f"  Учитель: {event.teacher}")

    if event.is_cancelled:
        print("  ⚠️ ОТМЕНЕН")

    if event.homework:
        print(f"  ДЗ: {event.homework.get('description')}")
```

---

## Userinfo

Модель базовой информации о пользователе из OAuth.

### Структура

```python
class Userinfo(BaseModel):
    user_id: int  # ID пользователя
    name: str  # Имя пользователя
    email: str  # Email
```

### Пример использования

```python
userinfo = await client.userinfo()
print(f"User: {userinfo.name} ({userinfo.email})")
```

---

## Работа с моделями

### Доступ к полям

Все модели поддерживают доступ через атрибуты:

```python
profile = await client.get_me()
print(profile.profile.first_name)  # Доступ через точку
```

### Преобразование в словарь

```python
profile = await client.get_me()
profile_dict = profile.model_dump()  # Преобразование в dict
```

### Преобразование в JSON

```python
import json

profile = await client.get_me()
profile_json = profile.model_dump_json()  # Преобразование в JSON строку
```

### Валидация данных

Pydantic автоматически валидирует данные при создании моделей:

```python
# Если API вернет невалидные данные, будет брошено исключение ValidationError
try:
    marks = await client.marks.get(from_date, to_date)
except ValidationError as e:
    print(f"Ошибка валидации: {e}")
```

## См. также

- [StudentClient](api/student_client.md) - Основной клиент
- [MarksClient](api/marks.md) - Работа с оценками
- [HomeworkClient](api/homeworks.md) - Работа с домашними заданиями
- [EventClient](api/events.md) - Работа с расписанием
