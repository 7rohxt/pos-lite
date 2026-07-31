# SQLAlchemy Models Notes

## What is a Model?

A **Model** is a Python class that maps to a database table.

```text
Python Class  ─────────► Database Table

User          ─────────► users
Product       ─────────► products
Sale          ─────────► sales
SaleItem      ─────────► sale_items
```

All models inherit from `Base`.

---

## Main Components

### `__tablename__`

Specifies the database table name.

```python
__tablename__ = "users"
```

---

### `mapped_column()`

Defines a database column.

```python
id = mapped_column(primary_key=True)
name = mapped_column(String)
price = mapped_column(Numeric(10, 2))
```

---

### `Mapped[...]`

Type hint for ORM fields.

```python
name: Mapped[str]
price: Mapped[Decimal]
```

---

### `relationship()`

Connects tables using ORM objects.

```python
User 1 ──────── * Sale

Sale 1 ──────── * SaleItem

Product 1 ───── * SaleItem
```

Use `back_populates` to make the relationship work in both directions.

---

## Foreign Keys

Creates links between tables.

```python
ForeignKey("users.id")
ForeignKey("products.id")
ForeignKey("sales.id")
```

---

## Why `Decimal` / `Numeric`?

Money should use:

```python
Decimal
Numeric(10, 2)
```

Avoid `float` due to precision errors.

---

## Why `SaleItem`?

A sale can contain multiple products.

```text
Sale #101

Coffee ×2
Tea ×1
Cake ×3
```

Each row becomes one `SaleItem`.

`unit_price` stores the **price at the time of sale**, so old invoices remain correct even if product prices change later.

---

# models/__init__.py

```python
from app.models.user import User
from app.models.product import Product
from app.models.sale import Sale, SaleItem
```

Purpose:

- Imports all models in one place.
- Registers them with SQLAlchemy.
- Allows:

```python
from app.models import User, Product, Sale
```

instead of importing from each file separately.

`__all__` defines the public exports of the package.