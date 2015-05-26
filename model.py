from datetime import datetime
from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/tap.db'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'tapeasebaby'

db = SQLAlchemy(app)

login_manager = LoginManager()

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(80))
    image_url = db.Column(db.String(80))
    is_enabled = db.Column(db.Boolean)
    create_date = db.Column(db.DateTime)
    access_token = db.Column(db.String(80))

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
    page_token = db.Column(db.String(80))
    base_url = db.Column(db.String(80))
    route_params = db.Column(db.String(80))
    query_params = db.Column(db.String(80))
    element_route = db.Column(db.String(80))
    node = db.Column(db.String(300))
    comment = db.Column(db.Text)
    create_date = db.Column(db.DateTime)

    def __init__(self, base_url, route_params, query_params, element_route, node, comment, page_token=None, create_date=None):
        if page_token is not None:
            self.page_token = page_token
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
           'page_token': self.page_token,
           'base_url': self.base_url,
           'route_params': self.route_params,
           'query_params': self.query_params,
           'element_route': self.element_route,
           'node': self.node,
           'comment': self.comment,
           'create_date': self.create_date.isoformat(),
       }