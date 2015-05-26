from datetime import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/tap.db'
db = SQLAlchemy(app)

class Tap(db.Model):

    __tablename__ = 'tap'

    id = db.Column(db.Integer, primary_key=True)
    base_url = db.Column(db.String(80))
    params = db.Column(db.String(80))
    element_route = db.Column(db.String(80))
    username = db.Column(db.String(80))
    image_url = db.Column(db.String(80))
    comment = db.Column(db.Text)
    date = db.Column(db.DateTime)

    def __init__(self, base_url, base_url, element_route, username, comment, image_url="", date=None):
        self.base_url = base_url
        self.params = params
        self.element_route = element_route
        self.username = username
        self.comment = comment
        self.image_url = image_url
        if date is None:
            date = datetime.utcnow()
        self.date = date

    @property
    def serialize(self):
       return {
           'id': self.id,
           'base_url': self.base_url,
           'params': self.params,
           'element_route': self.element_route,
           'username': self.username,
           'image_url': self.image_url,
           'comment': self.comment,
           'date': self.date.isoformat(),
       }