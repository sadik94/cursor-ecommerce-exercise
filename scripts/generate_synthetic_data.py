#!/usr/bin/env python3
"""
Generate synthetic e-commerce CSV files for the Cursor exercise.

Outputs (in /data/raw):
    - customers.csv
    - products.csv
    - orders.csv
    - order_items.csv
    - payments.csv
"""

from __future__ import annotations

import csv
import random
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable, List

from faker import Faker

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "data" / "raw"


@dataclass(frozen=True)
class Customer:
    id: str
    first_name: str
    last_name: str
    email: str
    country: str


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    category: str
    price: float


@dataclass(frozen=True)
class Order:
    id: str
    customer_id: str
    order_date: datetime
    status: str


@dataclass(frozen=True)
class OrderItem:
    id: str
    order_id: str
    product_id: str
    quantity: int
    unit_price: float


@dataclass(frozen=True)
class Payment:
    id: str
    order_id: str
    payment_method: str
    amount: float
    paid_at: datetime


def _write_csv(path: Path, headers: Iterable[str], rows: Iterable[Iterable[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.writer(fp)
        writer.writerow(headers)
        writer.writerows(rows)


def generate_customers(fake: Faker, count: int) -> List[Customer]:
    customers = []
    for _ in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name}.{last_name}.{uuid.uuid4().hex[:6]}@example.com".lower()
        customers.append(
            Customer(
                id=str(uuid.uuid4()),
                first_name=first_name,
                last_name=last_name,
                email=email,
                country=fake.country(),
            )
        )
    return customers


def generate_products(fake: Faker, count: int) -> List[Product]:
    categories = ["Electronics", "Apparel", "Home", "Sports", "Beauty"]
    products = []
    for _ in range(count):
        category = random.choice(categories)
        price = round(random.uniform(5, 500), 2)
        products.append(
            Product(
                id=str(uuid.uuid4()),
                name=fake.catch_phrase(),
                category=category,
                price=price,
            )
        )
    return products


def generate_orders(fake: Faker, customers: List[Customer], count: int) -> List[Order]:
    statuses = ["pending", "processing", "fulfilled", "cancelled"]
    now = datetime.utcnow()
    orders = []
    for _ in range(count):
        order_date = now - timedelta(days=random.randint(0, 180))
        orders.append(
            Order(
                id=str(uuid.uuid4()),
                customer_id=random.choice(customers).id,
                order_date=order_date,
                status=random.choices(statuses, weights=[0.2, 0.5, 0.25, 0.05])[0],
            )
        )
    return orders


def generate_order_items(orders: List[Order], products: List[Product]) -> List[OrderItem]:
    items = []
    for order in orders:
        for _ in range(random.randint(1, 4)):
            product = random.choice(products)
            quantity = random.randint(1, 5)
            items.append(
                OrderItem(
                    id=str(uuid.uuid4()),
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    unit_price=product.price,
                )
            )
    return items


def generate_payments(orders: List[Order], items: List[OrderItem]) -> List[Payment]:
    payment_methods = ["card", "paypal", "bank_transfer", "gift_card"]
    totals = {}
    for item in items:
        totals.setdefault(item.order_id, 0)
        totals[item.order_id] += item.quantity * item.unit_price

    payments = []
    for order in orders:
        payments.append(
            Payment(
                id=str(uuid.uuid4()),
                order_id=order.id,
                payment_method=random.choice(payment_methods),
                amount=round(totals.get(order.id, 0), 2),
                paid_at=order.order_date + timedelta(hours=random.randint(1, 48)),
            )
        )
    return payments


def main() -> None:
    fake = Faker()
    Faker.seed(1337)
    random.seed(1337)

    customers = generate_customers(fake, 200)
    products = generate_products(fake, 80)
    orders = generate_orders(fake, customers, 400)
    order_items = generate_order_items(orders, products)
    payments = generate_payments(orders, order_items)

    _write_csv(
        OUTPUT_DIR / "customers.csv",
        Customer.__dataclass_fields__.keys(),
        (vars(customer).values() for customer in customers),
    )
    _write_csv(
        OUTPUT_DIR / "products.csv",
        Product.__dataclass_fields__.keys(),
        (vars(product).values() for product in products),
    )
    _write_csv(
        OUTPUT_DIR / "orders.csv",
        ["id", "customer_id", "order_date", "status"],
        (
            [order.id, order.customer_id, order.order_date.isoformat(), order.status]
            for order in orders
        ),
    )
    _write_csv(
        OUTPUT_DIR / "order_items.csv",
        OrderItem.__dataclass_fields__.keys(),
        (vars(item).values() for item in order_items),
    )
    _write_csv(
        OUTPUT_DIR / "payments.csv",
        ["id", "order_id", "payment_method", "amount", "paid_at"],
        (
            [p.id, p.order_id, p.payment_method, f"{p.amount:.2f}", p.paid_at.isoformat()]
            for p in payments
        ),
    )

    print(f"Wrote {OUTPUT_DIR} with 5 CSV files.")


if __name__ == "__main__":
    main()

