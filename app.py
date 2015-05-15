import json
from flask import Flask
from flask import request
from flask import jsonify
from flask.ext.sqlalchemy import SQLAlchemy

from model import Annotation
from model import db

app = Flask(__name__)

@app.route("/annotation", methods=['GET', 'POST'])
def annotation():
    if request.method == 'POST':
        annotation = Annotation(
            pageid=request.get_json().get('pageid'),
            elementid=request.get_json().get('elementid'),
            username=request.get_json().get('username'),
            comment=request.get_json().get('comment'),
            date=request.get_json().get('date', None),
        )
        db.session.add(annotation)
        db.session.commit()
        return jsonify(annotation.serialize)
    else:
        results = Annotation.query \
            .filter_by(pageid=request.args.get('pageid', '')) \
            .order_by(Annotation.date) \
            .all()
        return jsonify(annotations=[a.serialize for a in results])

if __name__ == "__main__":
    app.run()