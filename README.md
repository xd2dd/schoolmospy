![Badge](https://img.shields.io/badge/version-0.2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)

# 📕 SchoolMosPy

SchoolMosPy is a lightweight async Python wrapper for school.mos.ru APIs. It provides a simple and intuitive interface to interact with the Moscow School Electronic Diary platform.

## ✨ Features

- **Async architecture** - built on `aiohttp` and `httpx` for high performance
- **Type safety** - uses `pydantic` for data validation
- **Simple API** - intuitive interface for working with data
- **Full-featured** - access to marks, homeworks, events, and profile data

## 📋 Requirements

- Python 3.12+
- aiohttp >= 3.12.15
- pydantic >= 2.11.9
- httpx >= 0.28.1

## 📦 Installation

```bash
pip install schoolmospy
```

## 🚀 Quick Start

```python
import asyncio
from schoolmospy import StudentClient

async def main():
    # Create client
    client = StudentClient(
        token="your_token",
        profile_id=12345
    )

    # Get profile
    profile = await client.get_me()
    print(f"Name: {profile.name}")

    # Get marks
    marks = await client.marks.get_marks(
        from_date="2024-01-01",
        to_date="2024-12-31"
    )

    # Get homeworks
    homeworks = await client.homeworks.get_homeworks(
        from_date="2024-01-01",
        to_date="2024-12-31"
    )

    # Get events/schedule
    events = await client.events.get_events(
        from_date="2024-01-01",
        to_date="2024-12-31"
    )

    await client.close()

asyncio.run(main())
```

## 📝 License

This project is licensed under the GPL-3.0 License. See the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Documentation](https://xd2dd.github.io/schoolmospy)
- [Report an Issue](https://github.com/xd2dd/schoolmospy/issues)

## 👨‍💻 Author

Ivan Kriventsev - [xd2dd@icloud.com](mailto:xd2dd@icloud.com)

---

⭐ If you like this project, please give it a star on GitHub!
