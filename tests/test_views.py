import json

from warehouse.config import db
from warehouse.models import Article


def test_index(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.mimetype == "text/html"


def test_health_check(client):
    endpoint = "health-check"
    for path in [f"{endpoint}", f"{endpoint}/"]:
        r = client.get(f"/api/{path}")
        assert r.status_code == 200


def test_upload_inventory(client):
    r = upload_fixture("inventory", client)

    assert r.json == {
        "inventory": [
            {"art_id": 1, "name": "leg", "stock": 12},
            {"art_id": 2, "name": "screw", "stock": 17},
            {"art_id": 3, "name": "seat", "stock": 2},
            {"art_id": 4, "name": "table top", "stock": 1},
        ]
    }
    # Increment stock.
    r = client.post(
        "/api/inventory",
        json={
            "inventory": [
                {"art_id": 1, "name": "leg", "stock": 8},
            ]
        },
    )
    assert r.json == {
        "inventory": [
            {"art_id": 1, "name": "leg", "stock": 20},
        ]
    }


def test_upload_products(client):
    upload_fixture("inventory", client)
    r = upload_fixture("products", client)

    assert r.json == {
        "products": [
            {
                "name": "Dining Chair",
                "contain_articles": [
                    {"amount_of": 4, "art_id": 1},
                    {"amount_of": 8, "art_id": 2},
                    {"amount_of": 1, "art_id": 3},
                ],
            },
            {
                "name": "Dining Table",
                "contain_articles": [
                    {"amount_of": 4, "art_id": 1},
                    {"amount_of": 8, "art_id": 2},
                    {"amount_of": 1, "art_id": 4},
                ],
            },
        ]
    }
    # Reject unknown article.
    r = client.post(
        "/api/products",
        json={
            "products": [
                {
                    "name": "Dining Chair",
                    "contain_articles": [
                        {"amount_of": 4, "art_id": 99},
                    ],
                },
            ]
        },
    )
    assert r.status_code == 404


def test_get_products(client):
    upload_fixture("inventory", client)
    upload_fixture("products", client)

    r = client.get("/api/products")
    assert r.status_code == 200
    assert r.json == {
        "products": [
            {"name": "Dining Chair", "quantity": 2},
            {"name": "Dining Table", "quantity": 1},
        ],
    }


def test_sell_product(client):
    upload_fixture("inventory", client)
    upload_fixture("products", client)

    r = client.delete("/api/products", json={"name": "Dining Table"})
    assert r.status_code == 200

    for attr_id, stock in {1: 8, 2: 9, 3: 2, 4: 0}.items():
        assert db.session.get(Article, attr_id).stock == stock

    assert client.get("/api/products").json == {
        "products": [
            {"name": "Dining Chair", "quantity": 1},
            {"name": "Dining Table", "quantity": 0},
        ],
    }

    r = client.delete("/api/products", json={"name": "Dining Chair"})
    assert r.status_code == 200

    for attr_id, stock in {1: 4, 2: 1, 3: 1, 4: 0}.items():
        assert db.session.get(Article, attr_id).stock == stock

    assert client.get("/api/products").json == {
        "products": [
            {"name": "Dining Chair", "quantity": 0},
            {"name": "Dining Table", "quantity": 0},
        ],
    }

    r = client.delete("/api/products", json={"name": "Dining Chair"})
    assert r.status_code == 428  # Sold out.


def upload_fixture(name, client):
    with open(f"tests/fixtures/{name}.json") as f:
        return client.post(
            f"/api/{name}",
            json=json.load(f),
        )
