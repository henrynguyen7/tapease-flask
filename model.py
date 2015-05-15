from datetime import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/annotation.db'
db = SQLAlchemy(app)

class Annotation(db.Model):

    __tablename__ = 'annotation'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(80))
    pageid = db.Column(db.String(80))
    elementid = db.Column(db.String(80))
    username = db.Column(db.String(80))
    imageurl = db.Column(db.String(80))
    comment = db.Column(db.Text)
    date = db.Column(db.DateTime)

    def __init__(self, pageid, elementid, username, comment, imageurl="", date=None):
        self.uid = pageid + "." + elementid
        self.pageid = pageid
        self.elementid = elementid
        self.username = username
        self.comment = comment
        self.imageurl = imageurl
        if date is None:
            date = datetime.utcnow()
        self.date = date

    @property
    def serialize(self):
       return {
           'id': self.id,
           'uid': self.uid,
           'pageid': self.pageid,
           'elementid': self.elementid,
           'username': self.username,
           'imageurl': self.imageurl,
           'comment': self.comment,
           'date': self.date.isoformat(),
       }