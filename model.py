#!/usr/bin/env python

from datetime import datetime

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tapeasedb.sqlite'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'tapeasebaby'

db = SQLAlchemy(app)


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(80))
    image_url = db.Column(db.String(80))
    is_enabled = db.Column(db.Boolean)
    create_date = db.Column(db.DateTime)

    def __init__(self, email, password, name="", image_url="", is_enabled=True):
        self.email = email
        self.hash_password(password)
        self.name = name
        self.image_url = image_url
        self.is_enabled = is_enabled
        self.create_date = datetime.utcnow()

    @property
    def serialize(self):
       return {
           'id': self.id,
           'email': self.email,
           'name': self.name,
           'image_url': self.image_url,
           'is_enabled': self.is_enabled,
           'create_date': self.create_date.isoformat(),
       }

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user


class Tap(db.Model):

    __tablename__ = 'tap'

    id = db.Column(db.Integer, primary_key=True)
    page_token = db.Column(db.String(80))
    page_uid = db.Column(db.String(80))
    element_route = db.Column(db.String(80))
    node = db.Column(db.String(300))
    comment = db.Column(db.Text)
    create_date = db.Column(db.DateTime)

    def __init__(self, page_uid, element_route, node, comment, page_token=None):
        if page_token is not None:
            self.page_token = page_token
        self.page_uid = page_uid
        self.element_route = element_route
        self.node = node
        self.comment = comment
        self.create_date = datetime.utcnow()

    @property
    def serialize(self):
       return {
           'id': self.id,
           'page_token': self.page_token,
           'page_uid': self.page_uid,
           'element_route': self.element_route,
           'node': self.node,
           'comment': self.comment,
           'create_date': self.create_date.isoformat(),
       }