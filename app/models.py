from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request
from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin
import hashlib

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.get_avatar()

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True)
    pass_hash = db.Column(db.String(256), nullable=False)
    location = db.Column(db.String(128), nullable=False)
    avatar_hash = db.Column(db.String(128))
    profile_pic = db.Column(db.String(128))
    country = db.Column(db.String(128))
    role = db.Column(db.String(32), nullable=False)
    products = db.relationship('Product', backref='user', lazy='dynamic', cascade="all, delete")
    carts = db.relationship('Cart', backref='owner', lazy='dynamic', cascade="all, delete")

    @property
    def password(self):
        raise AttributeError("Password not readable")

    @password.setter
    def password(self, password):
        self.pass_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_hash, password)

    def get_avatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default, rating=rating)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(32))
    price = db.Column(db.Integer, nullable=False)
    image_link = db.Column(db.String(128))
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(32), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cart_on = db.relationship('Cart', backref='product', lazy='dynamic', cascade="all, delete")

class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
