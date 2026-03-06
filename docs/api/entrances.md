# EntrancesClient

`EntrancesClient` - клиент для получения длительности пребывания ученика в школе (вход/выход по дням).

## Доступ

Доступ к `EntrancesClient` осуществляется через свойство `entrances` объекта `StudentClient`:

```python
from schoolmospy import StudentClient

client = StudentClient(token="ваш_токен", profile_id=12345)
entrances_client = client.entrances
```

## Методы

### `get_visit_durations()`

Получить историю входов/выходов и длительность пребывания за период.

```python
async def get_visit_durations(
    person_id: str,
    from_date: date | datetime,
    to_date: date | datetime,
    role_id: str = "7:1"
) -> VisitDurations
```

#### Параметры

| Параметр | Тип | Описание |
|----------|-----|----------|
| `person_id` | `str` | GUID ученика (`contingent_guid`) |
| `from_date` | `date \| datetime` | Начало периода (включительно) |
| `to_date` | `date \| datetime` | Конец периода (включительно) |
| `role_id` | `str` | Значение заголовка `x-mes-roleid` |

#### Возвращает

`VisitDurations` - модель Pydantic с массивом дней и посещений.

#### Пример

```python
from datetime import date
from schoolmospy import StudentClient

async def main():
    client = StudentClient(token="ваш_токен", profile_id=12345)

    profile = await client.get_me()
    person_id = profile.children[0].contingent_guid

    durations = await client.entrances.get_visit_durations(
        person_id=person_id,
        from_date=date(2026, 3, 2),
        to_date=date(2026, 3, 8),
    )

    for day in durations.payload:
        print(day.date)
        for visit in day.visits:
            print(f"  {visit.in_time} -> {visit.out_time} ({visit.duration})")
```

## См. также

- [StudentClient](student_client.md) - Основной клиент
- [Модели](../models.md) - Подробное описание моделей данных
