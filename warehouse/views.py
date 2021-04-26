import os
import sys

from flask import request, send_file

from sqlalchemy.sql import text

from .config import app, db, static_dir
from .models import Article, Product, ProductArticle


@app.route("/")
def index():
    """
    Return the landing page.
    """
    return send_file(os.path.join(static_dir, "index.html"))


@app.route("/api/health-check")
def health_check():
    """
    Get the operational status of this application and an indication
    of its ability to connect to downstream dependent services.
    """
    db.session.query(text("1")).from_statement(text("SELECT 1")).all()
    return {}


@app.route("/api/inventory", methods=["POST"])
def upload_inventory():
    """
    Upload inventory with the following format:
        {
            "inventory": [
                {
                    "art_id": 1,
                    "name": "leg",
                    "stock": 12
                },
                {
                    "art_id": 2,
                    "name": "screw",
                    "stock": 17
                },
                ...
            ]
        }
    :returns: The inventory with updated stock.
    """
    inventory = request.get_json(force=True).get("inventory")
    art_ids = []

    for item in inventory:
        art_id = int(item.get("art_id"))
        art_ids.append(art_id)

        a = db.session.get(Article, art_id)

        if not a:
            a = Article(art_id=art_id)

        a.name = item["name"]  # Update name.
        a.stock = int(item.get("stock", 0)) + (a.stock or 0)  # Increment stock.
        db.session.add(a)

    db.session.commit()

    updated_articles = db.session.query(Article).filter(Article.art_id.in_(art_ids)).all()
    return {"inventory": [a.as_dict() for a in updated_articles]}


@app.route("/api/products", methods=["POST"])
def upload_products():
    """
    Upload products with the following format:
        {
            "products": [
                {
                    "name": "Dining Chair",
                    "contain_articles": [
                        {
                            "art_id": 1,
                            "amount_of": 4
                        },
                        ...
                    ]
                },
                ...
            ]
        }
    :returns: The updated products.
    """
    products = request.get_json(force=True).get("products")
    prod_names = set()

    for item in products:
        name = item.get("name")
        p = db.session.get(Product, name)

        if not p:
            p = Product(name=name)

        p.contain_articles = []

        for subitem in item.get("contain_articles", []):
            art_id = int(subitem.get("art_id"))

            if not db.session.get(Article, art_id):
                return {"error": f"Article not found: {art_id}"}, 404

            p.contain_articles.append(
                ProductArticle(
                    prod_name=name,
                    art_id=art_id,
                    amount_of=int(subitem.get("amount_of")),
                )
            )
            prod_names.add(name)

        db.session.add(p)

    db.session.commit()

    updated_products = db.session.query(Product).filter(Product.name.in_(list(prod_names))).all()
    return {"products": [p.as_dict() for p in updated_products]}


@app.route("/api/products", methods=["GET"])
def get_products():
    """
    Get all products and quantity of each that is an available with the current inventory.

    :returns: A list of products with quantity.
        {
            "products": [
                {
                    "name": "Dining Table",
                    "quantity": 1
                },
                ...
            ]
        }
    """
    stock = {a.art_id: a.stock for a in db.session.query(Article).all()}
    all_products = db.session.query(Product).order_by(Product.name).all()

    for p in all_products:
        quantity = sys.maxsize

        for a in p.contain_articles:
            in_stock = stock[a.art_id]

            if in_stock >= a.amount_of:
                quantity = min(in_stock // a.amount_of, quantity)
            else:
                quantity = 0
                break

        p.quantity = quantity if quantity != sys.maxsize else 0

    return {
        "products": [
            {
                "name": p.name,
                "quantity": p.quantity,
            }
            for p in all_products
        ]
    }


@app.route("/api/products", methods=["DELETE"])
def sell_product():
    """
    Sell a product and update the inventory accordingly.
        {
            "name": "Dining Table"
        }
    """
    name = request.get_json(force=True).get("name")
    p = db.session.get(Product, name)

    if not p:
        return {"error": f"Product not found: {name}"}, 404

    for pa in p.contain_articles:
        a = db.session.get(Article, pa.art_id)

        if a.stock >= pa.amount_of:
            a.stock -= pa.amount_of
            db.session.add(a)
        else:
            return {"error": f"Product out of stock: {name}"}, 428

    db.session.commit()
    return {}
