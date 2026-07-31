# Configuration Notes

## What is `Settings`?

`Settings` inherits from `BaseSettings`.

It automatically:

- Reads values from `.env`
- Validates their types
- Makes them available throughout the app

Example:

```python
DATABASE_URL: str
```

Looks for:

```text
DATABASE_URL=sqlite:///todos.db
```

---

## `settings = Settings()`

Creates a **Settings object**.

During creation it:

1. Reads `.env`
2. Validates values
3. Stores them

Now anywhere in the project:

```python
from app.core.config import settings

settings.DATABASE_URL
```

---

## Why a separate `config.py`?

Without it:

```text
database.py  → DATABASE_URL = os.getenv(...)
auth.py      → SECRET_KEY = os.getenv(...)
email.py     → SMTP_USER = os.getenv(...)
```

Configuration becomes scattered.

With `config.py`:

```text
config.py
      │
      ▼
settings
      │
      ├── DATABASE_URL
      ├── SECRET_KEY
      └── SMTP_USER
```

**One place for all application configuration.**