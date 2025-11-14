PYTHON ?= python3
RAW_DIR := data/raw
DB_PATH := data/sqlite/ecommerce.db

.PHONY: data ingest analyze test clean-db

data:
	$(PYTHON) scripts/generate_synthetic_data.py --output-dir $(RAW_DIR)

ingest: data
	$(PYTHON) scripts/ingest_to_sqlite.py --raw-dir $(RAW_DIR) --db-path $(DB_PATH)

analyze: ingest
	sqlite3 $(DB_PATH) < sql/customer_revenue.sql

test:
	$(PYTHON) -m pytest

clean-db:
	rm -f $(DB_PATH)

