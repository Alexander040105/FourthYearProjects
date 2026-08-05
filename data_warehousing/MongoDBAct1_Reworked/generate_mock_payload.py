"""
Generate a deterministic 1,500-document mock JSON payload for the
raw checkout landing collection.
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

SOURCE_COUNTS = {
    "WEB_STORE": 820,
    "POS_TERMINALS": 450,
    "MOBILE_APP": 230,
}

EVENT_TYPES = ["checkout", "purchase", "refund", "cart_update"]

PAYMENT_METHODS = {
    "WEB_STORE": ["credit_card", "paypal", "cod", "gcash"],
    "POS_TERMINALS": ["cash", "card"],
    "MOBILE_APP": ["gcash", "maya", "card"],
}

REGIONS = ["NCR", "Luzon", "Visayas", "Mindanao"]
DEVICES = ["iOS", "Android"]

DATE_FORMATS = [
    "%Y-%m-%dT%H:%M:%SZ",
    "%m/%d/%Y %H:%M:%S",
    "%d-%m-%Y %H:%M:%S",
    "%Y/%m/%d %H:%M:%S",
]


def random_timestamp() -> str:
    dt = datetime.utcnow() - timedelta(
        days=random.randint(0, 365),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )
    return dt.strftime(random.choice(DATE_FORMATS))


def make_web_store(idx: int) -> dict:
    return {
        "order_id": f"WS-{idx:06d}",
        "product_id": f"P-{random.randint(1000, 9999)}",
        "quantity": random.randint(1, 10),
        "total": round(random.uniform(10.0, 500.0), 2),
        "payment_method": random.choice(PAYMENT_METHODS["WEB_STORE"]),
        "customer_id": f"C-{random.randint(10000, 99999)}",
        "region": random.choice(REGIONS),
        "timestamp": random_timestamp(),
    }


def make_pos(idx: int) -> dict:
    items = [
        {
            "sku": f"SKU-{random.randint(1000, 9999)}",
            "qty": random.randint(1, 5),
            "price": round(random.uniform(5.0, 100.0), 2),
        }
        for _ in range(random.randint(1, 5))
    ]
    return {
        "transaction_id": f"POS-{idx:06d}",
        "terminal_id": f"T-{random.randint(1, 999)}",
        "store_id": f"S-{random.randint(1, 200)}",
        "items": items,
        "total": round(sum(i["qty"] * i["price"] for i in items), 2),
        "payment_method": random.choice(PAYMENT_METHODS["POS_TERMINALS"]),
        "timestamp": random_timestamp(),
    }


def make_mobile(idx: int) -> dict:
    cart = [
        {
            "item_id": f"I-{random.randint(1000, 9999)}",
            "qty": random.randint(1, 3),
            "price": round(random.uniform(10.0, 200.0), 2),
        }
        for _ in range(random.randint(1, 5))
    ]
    return {
        "session_id": f"M-{idx:06d}",
        "user_id": f"U-{random.randint(1000, 99999)}",
        "device_os": random.choice(DEVICES),
        "cart": cart,
        "total": round(sum(c["qty"] * c["price"] for c in cart), 2),
        "payment_method": random.choice(PAYMENT_METHODS["MOBILE_APP"]),
        "timestamp": random_timestamp(),
    }


PAYLOAD_BUILDERS = {
    "WEB_STORE": make_web_store,
    "POS_TERMINALS": make_pos,
    "MOBILE_APP": make_mobile,
}


def build_document(counter: int, source: str) -> dict:
    record = {
        "source": source,
        "eventType": random.choice(EVENT_TYPES),
        "payload": PAYLOAD_BUILDERS[source](counter),
    }

    # Sprinkle a small amount of data quality issues for auditing.
    if random.random() < 0.05:
        anomaly = random.choice(
            [
                "missing_eventType",
                "missing_payload",
                "payload_array",
                "missing_total",
                "missing_timestamp",
                "malformed_timestamp",
            ]
        )

        if anomaly == "missing_eventType":
            del record["eventType"]
        elif anomaly == "missing_payload":
            record["payload"] = None
        elif anomaly == "payload_array":
            record["payload"] = [record["payload"]]
        elif (
            anomaly == "missing_total"
            and isinstance(record["payload"], dict)
            and "total" in record["payload"]
        ):
            del record["payload"]["total"]
        elif (
            anomaly == "missing_timestamp"
            and isinstance(record["payload"], dict)
            and "timestamp" in record["payload"]
        ):
            del record["payload"]["timestamp"]
        elif (
            anomaly == "malformed_timestamp"
            and isinstance(record["payload"], dict)
            and "timestamp" in record["payload"]
        ):
            record["payload"]["timestamp"] = "not-a-valid-date"

    return record


def main() -> None:
    output_path = Path(__file__).with_name("mock_payload.json")
    documents = []
    counter = 0

    for source, count in SOURCE_COUNTS.items():
        for _ in range(count):
            counter += 1
            documents.append(build_document(counter, source))

    # Final sanity check for totals.
    assert len(documents) == sum(SOURCE_COUNTS.values()), "Document count mismatch"

    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(documents, fh, indent=2)

    print(f"Generated {len(documents):,} documents -> {output_path}")


if __name__ == "__main__":
    main()
