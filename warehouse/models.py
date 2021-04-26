from sqlalchemy import orm

from .config import db


class Article(db.Model):
    __table_args__ = {"extend_existing": True}

    art_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ProductArticle(db.Model):
    __table_args__ = {"extend_existing": True}

    prod_name = db.Column("prod_name", db.String, db.ForeignKey("product.name"), primary_key=True)
    art_id = db.Column("art_id", db.Integer, db.ForeignKey("article.art_id"), primary_key=True)
    amount_of = db.Column("amount_of", db.Integer, nullable=False, default=0)

    def as_dict(self):
        excluded = ["prod_name"]
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in excluded}


class Product(db.Model):
    __table_args__ = {"extend_existing": True}

    name = db.Column(db.String(255), primary_key=True)
    contain_articles = orm.relationship(
        "ProductArticle",
        backref="product",
        primaryjoin=(name == ProductArticle.prod_name),
        cascade="save-update, merge, delete, delete-orphan",
    )

    def as_dict(self):
        obj = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        obj["contain_articles"] = [pa.as_dict() for pa in self.contain_articles]
        return obj
