#!/usr/bin/env python3.7
"""
Mastering Object-Oriented Python 2e

Code Examples for Mastering Object-Oriented Python 2nd Edition

Chapter 12. Example 2.
"""

# BLOB Mapping
# =========================

# Adding Decimal data to a SQLite database.
import sqlite3
import decimal


def adapt_currency(value):
    return str(value)


sqlite3.register_adapter(decimal.Decimal, adapt_currency)


def convert_currency(bytes):
    return decimal.Decimal(bytes.decode())


sqlite3.register_converter("DECIMAL", convert_currency)

# When we define a table, we must use the type "decimal"
# to get two-digit decimal values.

decimal_cleanup = """
DROP TABLE IF EXISTS budget
"""

decimal_ddl = """
CREATE TABLE budget(
    year INTEGER,
    month INTEGER,
    category TEXT,
    amount DECIMAL
)
"""
insert_budget = """
INSERT INTO budget(year, month, category, amount) VALUES(:year, :month, :category, :amount)
"""
query_budget = """
SELECT * FROM budget
"""

test_decimal = """
>>> from pathlib import Path
>>> database = sqlite3.connect(
...    Path.cwd() / "data" / "ch12_blog.db", 
...    detect_types=sqlite3.PARSE_DECLTYPES  # Required to include additional types
... )  # type: ignore

>>> _ = database.execute(decimal_cleanup)
>>> _ = database.execute(decimal_ddl)

>>> _ = database.execute(
...    insert_budget,
...    dict(year=2013, month=1, category="fuel", amount=decimal.Decimal("256.78")),
... )
>>> _ = database.execute(
...    insert_budget,
...    dict(year=2013, month=2, category="fuel", amount=decimal.Decimal("287.65")),
... )

>>> for row in database.execute(query_budget):
...    print(row)
(2013, 1, 'fuel', Decimal('256.78'))
(2013, 2, 'fuel', Decimal('287.65'))
>>> database.close()
"""

__test__ = {name: value for name, value in locals().items() if name.startswith("test_")}

if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
