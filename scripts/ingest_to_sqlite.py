#!/usr/bin/env python3
"""
Load the generated CSV data into a SQLite database.
"""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
DB_PATH = ROOT / "data" / "sqlite" / "ecommerce.db"


CREATE_STATEMENTS = [
    """
    CREATE TABLE customers (
        id TEXT PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        country TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE products (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL
    );
    """,
    """
    CREATE TABLE orders (
        id TEXT PRIMARY KEY,
        customer_id TEXT NOT NULL REFERENCES customers(id),
        order_date TEXT NOT NULL,
        status TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE order_items (
        id TEXT PRIMARY KEY,
        order_id TEXT NOT NULL REFERENCES orders(id),
        product_id TEXT NOT NULL REFERENCES products(id),
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL
    );
    """,
    """
    CREATE TABLE payments (
        id TEXT PRIMARY KEY,
        order_id TEXT NOT NULL REFERENCES orders(id),
        payment_method TEXT NOT NULL,
        amount REAL NOT NULL,
        paid_at TEXT NOT NULL
    );
    """,
]


def _load_csv_rows(path: Path):
    with path.open("r", encoding="utf-8") as fp:
        reader = csv.DictReader(fp)
        yield from reader


def _insert_many(conn: sqlite3.Connection, table: str, rows):
    rows = list(rows)
    if not rows:
        return
    columns = rows[0].keys()
    placeholders = ",".join(["?"] * len(columns))
    sql = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
    conn.executemany(sql, ([row[col] for col in columns] for row in rows))


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    try:
        for statement in CREATE_STATEMENTS:
            conn.execute(statement)

        _insert_many(conn, "customers", _load_csv_rows(RAW_DIR / "customers.csv"))
        _insert_many(conn, "products", _load_csv_rows(RAW_DIR / "products.csv"))
        _insert_many(conn, "orders", _load_csv_rows(RAW_DIR / "orders.csv"))
        _insert_many(conn, "order_items", _load_csv_rows(RAW_DIR / "order_items.csv"))
        _insert_many(conn, "payments", _load_csv_rows(RAW_DIR / "payments.csv"))

        conn.commit()
        print(f"Ingested CSV data into {DB_PATH}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

