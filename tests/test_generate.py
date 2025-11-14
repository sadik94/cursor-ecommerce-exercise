import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_synthetic_data.py"


def _count_rows(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as fp:
        reader = csv.reader(fp)
        return sum(1 for _ in reader)


def test_generate_creates_all_files(tmp_path):
    output_dir = tmp_path / "raw"
    cmd = [
        sys.executable,
        str(SCRIPT),
        "--customers",
        "5",
        "--products",
        "4",
        "--orders",
        "8",
        "--max-items-per-order",
        "2",
        "--seed",
        "123",
        "--output-dir",
        str(output_dir),
    ]
    subprocess.run(cmd, check=True, cwd=ROOT)

    expected_files = [
        "customers.csv",
        "products.csv",
        "orders.csv",
        "order_items.csv",
        "payments.csv",
    ]
    for filename in expected_files:
        file_path = output_dir / filename
        assert file_path.exists(), f"{filename} missing"
        assert _count_rows(file_path) > 1, f"{filename} should contain data rows"

