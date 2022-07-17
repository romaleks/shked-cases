from . import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)

class User_price(db.Model):
    __tablename__ = 'user_price'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String)
    price = db.Column(db.Integer)

class User_info(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String)
    item = db.Column(db.String)
    opened_at = db.Column(db.DateTime)

class Case(db.Model):
    __tablename__ = 'case'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    icon_url = db.Column(db.String)

class CSGO_Item(db.Model):
    __tablename__ = 'csgo_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    rarity = db.Column(db.String)
    quality = db.Column(db.String)
    stattrak = db.Column(db.Boolean)
    case = db.Column(db.String)
    icon_url = db.Column(db.String)
    price = db.Column(db.Integer)
    priority = db.Column(db.Integer)