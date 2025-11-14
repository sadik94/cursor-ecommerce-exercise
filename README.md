# Cursor E‑Commerce Data Exercise

This repository contains a small workflow that satisfies the exercise outlined in the prompt:

1. Generate roughly five synthetic e-commerce data files.
2. Ingest the generated data into a SQLite database.
3. Run an example SQL query that joins multiple tables and produces an aggregated output.

## Requirements

- Python 3.11+
- `pip` (for installing the lone dependency, `faker`)

Install dependencies:

```bash
cd /Users/sadikb/Desktop/diligent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 1. Generate Synthetic Data

Run the generator script. It writes five CSV files to `data/raw` by default:

```bash
python scripts/generate_synthetic_data.py
```

Generated files:

- `customers.csv`
- `products.csv`
- `orders.csv`
- `order_items.csv`
- `payments.csv`

## 2. Ingest Data Into SQLite

The ingestion script creates `data/sqlite/ecommerce.db` (overwriting if it exists) and loads each CSV into normalized tables.

```bash
python scripts/ingest_to_sqlite.py
```

## 3. Run Joined SQL Query

Use the provided SQL file that joins orders, customers, order items, and products to compute revenue per customer:

```bash
sqlite3 data/sqlite/ecommerce.db < sql/customer_revenue.sql
```

Adjust the SQL or build upon it to explore additional metrics as needed.

