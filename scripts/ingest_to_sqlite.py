#!/usr/bin/env python3
"""
Load the generated CSV data into a SQLite database.
"""

from __future__ import annotations

import argparse
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


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest CSV data into SQLite.")
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=RAW_DIR,
        help="Directory containing generated CSV files",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=DB_PATH,
        help="Path to output SQLite database",
    )
    parser.add_argument(
        "--keep-existing",
        action="store_true",
        help="If set, reuse existing database file instead of deleting",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    raw_dir = args.raw_dir.resolve()
    db_path = args.db_path.resolve()

    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists() and not args.keep_existing:
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    try:
        for statement in CREATE_STATEMENTS:
            conn.execute(statement)

        _insert_many(conn, "customers", _load_csv_rows(raw_dir / "customers.csv"))
        _insert_many(conn, "products", _load_csv_rows(raw_dir / "products.csv"))
        _insert_many(conn, "orders", _load_csv_rows(raw_dir / "orders.csv"))
        _insert_many(
            conn, "order_items", _load_csv_rows(raw_dir / "order_items.csv")
        )
        _insert_many(conn, "payments", _load_csv_rows(raw_dir / "payments.csv"))

        conn.commit()
        print(f"Ingested CSV data into {db_path}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

