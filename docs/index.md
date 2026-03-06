# Документация SchoolMosPy

Добро пожаловать в **SchoolMosPy** - легковесную асинхронную Python библиотеку для работы с API school.mos.ru.

![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)

## Обзор

SchoolMosPy предоставляет простой и интуитивный интерфейс для взаимодействия с платформой МЭШ. Библиотека позволяет программно получать информацию об ученике, оценках, домашних заданиях, расписании и питании.

## Основные возможности

- **🚀 Асинхронная архитектура** - Построена на `httpx` для высокой производительности и эффективных асинхронных операций
- **🔒 Типизация** - Использует `pydantic` для надежной валидации данных и подсказок типов
- **🎯 Простой API** - Чистый и интуитивный интерфейс для работы со школьными данными
- **📚 Полнофункциональная** - Полный доступ к оценкам, домашним заданиям, событиям, питанию и данным профиля
- **⚡ Легковесная** - Минимум зависимостей и небольшой размер

## Установка

Установите SchoolMosPy с помощью pip:

```bash
pip install schoolmospy
```

## Требования

- Python 3.12 или выше
- httpx >= 0.28.1
- pydantic >= 2.11.9

## Быстрый пример

```python
import asyncio
from datetime import datetime
from schoolmospy import StudentClient

async def main():
    # Инициализация клиента
    client = StudentClient(
        token="ваш_токен",
        profile_id=12345
    )

    # Получение информации о профиле
    profile = await client.get_me()
    print(f"Ученик: {profile.profile.first_name} {profile.profile.last_name}")

    # Получение оценок за период
    marks = await client.marks.get(
        from_date=datetime(2024, 1, 1),
        to_date=datetime(2024, 12, 31)
    )
    print(f"Всего оценок: {len(marks.payload)}")

asyncio.run(main())
```

## Начало работы

Чтобы начать работу с SchoolMosPy, ознакомьтесь с [руководством по быстрому старту](quickstart.md).

## Документация API

Изучите подробную документацию API:

- [StudentClient](api/student_client.md) - Основной клиент для работы с данными ученика
- [MarksClient](api/marks.md) - Доступ к оценкам ученика
- [HomeworkClient](api/homeworks.md) - Получение домашних заданий
- [EventClient](api/events.md) - Получение расписания и событий
- [MealsClient](api/meals.md) - Получение школьного питания

## Поддержка

- **Документация**: [https://xd2dd.github.io/schoolmospy](https://xd2dd.github.io/schoolmospy)
- **Проблемы**: [GitHub Issues](https://github.com/xd2dd/schoolmospy/issues)
- **Исходный код**: [GitHub Repository](https://github.com/xd2dd/schoolmospy)

## Лицензия

Этот проект лицензирован под GPL-3.0 License. Подробности в файле LICENSE.

## Автор

**Ivan Kriventsev**
Email: [xd2dd@icloud.com](mailto:xd2dd@icloud.com)
