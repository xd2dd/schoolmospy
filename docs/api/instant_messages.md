# InstantMessagesClient

`InstantMessagesClient` - клиент для получения ленты уведомлений.

## Доступ

Доступ к `InstantMessagesClient` осуществляется через свойство `instant_messages` объекта `StudentClient`:

```python
from schoolmospy import StudentClient

client = StudentClient(token="ваш_токен", profile_id=12345)
messages_client = client.instant_messages
```

## Методы

### `get_feed()`

Получить страницу ленты уведомлений.

```python
async def get_feed(
    page: int = 1,
    npp: int = 10,
    role_id: str = "7:1"
) -> InstantMessagesFeed
```

#### Параметры

| Параметр | Тип | Описание |
|----------|-----|----------|
| `page` | `int` | Номер страницы |
| `npp` | `int` | Количество уведомлений на странице |
| `role_id` | `str` | Значение заголовка `x-mes-roleid` |

#### Возвращает

`InstantMessagesFeed` - модель Pydantic со списком уведомлений (`data`).

#### Пример

```python
feed = await client.instant_messages.get_feed(page=1, npp=10)

for item in feed.data:
    print(item.created_at, item.title)
```

## См. также

- [StudentClient](student_client.md) - Основной клиент
- [Модели](../models.md) - Подробное описание моделей данных
