# SQLAlchemy Session Notes

## What is a Session?

A **Session** represents **one unit of work** with the database.

Every HTTP request gets its **own Session**.

```text
Create Session
      │
      ▼
Query
      │
      ▼
Modify Objects
      │
      ▼
Commit
      │
      ▼
Close
```

---

## Why do we need a Session?

Think of it like an online shopping cart.

```text
Open Cart
      │
      ▼
Add Item
      │
      ▼
Remove Item
      │
      ▼
Change Quantity
      │
      ▼
Checkout
```

The cart keeps track of all your changes.

Only when you **Checkout** are the changes finalized.

Similarly, a Session tracks all database changes and saves them only when:

```python
db.commit()
```

---

## Why not use the Engine directly?

**Engine**
- Knows how to communicate with the database.
- Executes SQL.
- Does **not** track object changes.

**Session**
- Tracks Python objects.
- Knows what was added, updated, or deleted.
- Decides when to `commit()` or `rollback()`.
- Uses the Engine to execute SQL.

Flow:

```text
Python Objects
      │
      ▼
Session (tracks changes)
      │
      ▼
Engine (executes SQL)
      │
      ▼
Database
```

---

## Request Flow

Every request creates a new Session.

```text
Client Request
      │
      ▼
get_db()
      │
      ▼
SessionLocal()
      │
      ▼
Database Session
      │
      ▼
Route Handler
      │
      ▼
db.query(...)
db.add(...)
db.commit()
      │
      ▼
Route returns response
      │
      ▼
db.close()
```

## Remember

- **One request = One Session**
- **One Session = One unit of work**
- **Engine communicates with the DB**
- **Session tracks changes and uses the Engine**