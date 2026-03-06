# GamificationClient

`GamificationClient` - клиент для работы с подарками МЭШ (каталог и подарки профиля).

## Доступ

Доступ к `GamificationClient` осуществляется через свойство `gamification` объекта `StudentClient`:

```python
from schoolmospy import StudentClient

client = StudentClient(token="ваш_токен", profile_id=12345)
gifts_client = client.gamification
```

## Методы

### `get_profile()`

Получить профиль геймификации по `person_id` (contingent GUID).

```python
async def get_profile(person_id: str) -> GamificationProfile
```

### `search_rewards()`

Поиск доступных подарков в каталоге.

```python
async def search_rewards(
    page_number: int = 1,
    page_size: int = 20,
    reward_types: list[str] | None = None,
    statuses: list[str] | None = None,
    is_empty_hidden: bool = True
) -> RewardsSearchResponse
```

### `get_profile_rewards()`

Получить подарки, связанные с профилем.

```python
async def get_profile_rewards(
    profile_id: int,
    from_scope: str = "ALL",
    to_scope: str = "ME",
    page_number: int = 1,
    page_size: int = 10,
    order_by: str = "purchasedAt",
    direction: str = "DESC"
) -> ProfileRewardsResponse
```

## Пример

```python
gamification_profile = await client.gamification.get_profile(
    person_id=profile.children[0].contingent_guid
)

catalog = await client.gamification.search_rewards(
    reward_types=["GIFT"],
    statuses=["ACTIVE"],
)

my_rewards = await client.gamification.get_profile_rewards(
    profile_id=gamification_profile.id,
    from_scope="ALL",
    to_scope="ME",
)

print(len(catalog.content), len(my_rewards.content))
```

## См. также

- [StudentClient](student_client.md) - Основной клиент
- [Модели](../models.md) - Подробное описание моделей данных
