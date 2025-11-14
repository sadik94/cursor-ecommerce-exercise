# Cursor E‑Commerce Data Exercise

This repository contains a small workflow that satisfies the Cursor exercise:

1. Generate roughly five synthetic e-commerce data files.
2. Ingest the generated data into a SQLite database.
3. Run SQL that joins multiple tables and returns useful summaries.

## Requirements

- Python 3.11+
- `pip`
- `make` (optional but convenient)

Install dependencies (Faker + pytest):

```bash
cd /Users/sadikb/Desktop/diligent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Quickstart (recommended)

```bash
make analyze
```

This single command regenerates CSV files, ingests them into SQLite, and executes the default customer revenue SQL.

Other handy targets:

- `make data` – generate CSVs only
- `make ingest` – regenerate CSVs and rebuild the database
- `make test` – run the pytest smoke tests

## CLI usage

### 1. Generate synthetic data

```bash
python scripts/generate_synthetic_data.py \
  --customers 250 \
  --products 90 \
  --orders 500 \
  --max-items-per-order 5 \
  --seed 1337 \
  --output-dir data/raw
```

Arguments let you control dataset size, output directory, and determinism. By default the script writes five CSV files (`customers`, `products`, `orders`, `order_items`, `payments`) into `data/raw`.

### 2. Ingest data into SQLite

```bash
python scripts/ingest_to_sqlite.py \
  --raw-dir data/raw \
  --db-path data/sqlite/ecommerce.db
```

Use `--keep-existing` if you want to append to an existing database file instead of recreating it.

### 3. Run SQL queries

```bash
sqlite3 data/sqlite/ecommerce.db < sql/customer_revenue.sql
sqlite3 data/sqlite/ecommerce.db < sql/category_revenue.sql
```

- `sql/customer_revenue.sql` – lifetime value per customer (orders joined with customers/order items).
- `sql/category_revenue.sql` – total revenue and order counts by product category.

Feel free to add more SQL files and invoke them the same way.

## Tests

A light pytest suite (`tests/test_generate.py`) runs the generator with small record counts and verifies that all five CSV files are produced with data rows. Execute the suite with:

```bash
make test
```

