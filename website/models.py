from sqlalchemy import event
from . import db
from flask_login import UserMixin
from sqlalchemy import DateTime, Boolean
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(150), default='User')
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(300))
    nickname = db.Column(db.String(150))
    comments = db.relationship('Comment', backref='user', lazy=True, cascade="all, delete-orphan")
    carts = db.relationship('Cart', backref='user', lazy=True, cascade="all, delete-orphan")
    orders = db.relationship('Order', backref='user', lazy=True)
    messages = db.relationship('Message', backref='user', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return self.nickname

class Comment(db.Model):    
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    tovar_id = db.Column(db.Integer(), db.ForeignKey('tovar.id'))
    created_at = db.Column(DateTime, default=datetime.now)   
    
    def __repr__(self):
        return self.text

class Sklad(db.Model):
    __tablename__ = 'sklad'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(150), unique=True)
    tovary = db.relationship('Tovar', backref='sklad', lazy=True)

class Tovar(db.Model):
    __tablename__ = 'tovar'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), default='Mat', nullable=False)
    name = db.Column(db.String(150), unique=True)
    count = db.Column(db.Integer)
    cost = db.Column(db.Float)
    status = db.Column(db.String(20))
    color = db.Column(db.String(30))
    size = db.Column(db.String(20))
    thickness = db.Column(db.String(20)) 
    material = db.Column(db.String(20)) 
    base = db.Column(db.String(20))
    info = db.Column(db.String(500))
    sklad_id = db.Column(db.Integer, db.ForeignKey('sklad.id'), nullable=False, default=1)
    img_name = db.Column(db.String(500), unique=True)
    comments = db.relationship('Comment', backref='tovar', lazy=True, cascade = "all, delete-orphan")
    cart = db.relationship('Cart', backref='tovar', lazy=True, cascade = "all, delete-orphan")
    order = db.relationship('Order', backref='tovar', lazy=True, cascade = "all, delete-orphan")

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(150), db.ForeignKey('user.email'), nullable=False)
    tovar_name = db.Column(db.String(150), db.ForeignKey('tovar.name'), nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float, default=0)

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(200))
    nomerzakaza = db.Column(db.Integer)
    fio = db.Column(db.String(50))
    email = db.Column(db.String(150), db.ForeignKey('user.email'), nullable=False)
    telephone = db.Column(db.String(50))
    track_number = db.Column(db.String(200), default='Soon')
    receiving_point = db.Column(db.String(150), db.ForeignKey('point.id'))
    country = db.Column(db.String(30), default='Belarus')
    city = db.Column(db.String(20))
    street = db.Column(db.String(100))
    house = db.Column(db.String(10))
    flat = db.Column(db.String(10))
    comment = db.Column(db.String(200))
    promocod = db.Column(db.String(10))
    tovar_name = db.Column(db.String(150), db.ForeignKey('tovar.name'), nullable=False)
    price = db.Column(db.Float)
    tovar_quantity = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='In processing')
    created_at = db.Column(DateTime, default=datetime.now)
    point = db.relationship('Point', backref='order', lazy=True)

class Point(db.Model):
    __tablename__ = 'point'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String)
    street = db.Column(db.String)
    number = db.Column(db.Integer)

class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000))
    user_email = db.Column(db.Integer, db.ForeignKey('user.email'))
    created_at = db.Column(DateTime, default=datetime.now)
    category = db.Column(Boolean, default=False)

@event.listens_for(Order, 'after_update')
def after_status_change(mapper, connection, target):
    try:
        db.session.query(Order).filter(Order.nomerzakaza == target.nomerzakaza).update({"track_number": target.track_number})
        db.session.query(Order).filter(Order.nomerzakaza == target.nomerzakaza).update({"status": target.status})
        new_message = Message(
            text=f"Order status changed to {target.status}",
            user_email=target.email,
            created_at=datetime.now(),
            category=True
        )
        
        db.session.add(new_message)
    except Exception as e:
        db.session.rollback()
        raise e
    
