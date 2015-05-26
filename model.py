from datetime import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/tap.db'
db = SQLAlchemy(app)

secret_key = 'tapeasebaby'


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    name = db.Column(db.String(80))
    image_url = db.Column(db.String(80))
    is_enabled = db.Column(db.Boolean)
    create_date = db.Column(db.DateTime)
    access_token = db.Column(EncryptedType(db.String, secret_key))

    def __init__(self, email, password, name, image_url="", is_enabled=True, create_date=None):
        self.email = email
        self.password = password
        self.name = name
        self.image_url = image_url
        self.is_enabled = is_enabled
        if create_date is None:
            create_date = datetime.utcnow()
        self.create_date = create_date

    @property
    def serialize(self):
       return {
           'id': self.id,
           'email': self.email,
           'password': self.password,
           'name': self.name,
           'image_url': self.image_url,
           'is_enabled': self.is_enabled,
           'create_date': self.create_date.isoformat(),
       }


class Tap(db.Model):

    __tablename__ = 'tap'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey('user.id'))
    page_token = db.Column(db.String(80))
    base_url = db.Column(db.String(80))
    route_params = db.Column(db.String(80))
    query_params = db.Column(db.String(80))
    element_route = db.Column(db.String(80))
    node = db.Column(db.String(300))
    comment = db.Column(db.Text)
    create_date = db.Column(db.DateTime)

    def __init__(self, user_id, element_route, comment, page_token=None, base_url=None, route_params=None, query_params=None, create_date=None):
        self.user_id = user_id
        if page_token is not None:
            self.page_token = page_token
        elif base_url is not None:
            self.base_url = base_url
            self.route_params = route_params
            self.query_params = query_params
        self.element_route = element_route
        self.node = node
        self.comment = comment
        if create_date is None:
            create_date = datetime.utcnow()
        self.create_date = create_date

    @property
    def serialize(self):
       return {
           'id': self.id,
           'user_id': self.user_id,
           'page_token': self.page_token,
           'base_url': self.base_url,
           'route_params': self.route_params,
           'query_params': self.query_params,
           'element_route': self.element_route,
           'node': self.node,
           'comment': self.comment,
           'create_date': self.create_date.isoformat(),
       }