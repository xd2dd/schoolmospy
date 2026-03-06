# MealsClient

`MealsClient` - клиент для получения школьного питания (комплексов и позиций меню) на конкретную дату.

## Доступ

Доступ к `MealsClient` осуществляется через свойство `meals` объекта `StudentClient`:

```python
from schoolmospy import StudentClient

client = StudentClient(token="ваш_токен", profile_id=12345)
meals_client = client.meals
```

## Методы

### `get_complexes()`

Получить доступные комплексы питания для ученика на дату.

```python
async def get_complexes(
    on_date: date | datetime,
    person_id: str,
    row_limit: int = 27
) -> MealComplexes
```

#### Параметры

| Параметр | Тип | Описание |
|----------|-----|----------|
| `on_date` | `date \| datetime` | Дата, на которую нужно меню |
| `person_id` | `str` | GUID ученика (`contingent_guid`) |
| `row_limit` | `int` | Ограничение количества строк ответа |

#### Возвращает

`MealComplexes` - модель Pydantic, содержащая список комплексов питания.

#### Пример

```python
from datetime import date
from schoolmospy import StudentClient

async def main():
    client = StudentClient(token="ваш_токен", profile_id=12345)

    profile = await client.get_me()
    person_id = profile.children[0].contingent_guid

    meals = await client.meals.get_complexes(
        on_date=date(2026, 3, 10),
        person_id=person_id,
    )

    for complex_item in meals.items:
        print(f"{complex_item.name}: {complex_item.price / 100:.2f} ₽")
        for item in complex_item.items:
            print(f"  - {item.name}")
```

## См. также

- [StudentClient](student_client.md) - Основной клиент
- [Модели](../models.md) - Подробное описание моделей данных
