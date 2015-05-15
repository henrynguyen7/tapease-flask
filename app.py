import json
from flask import Flask, request, jsonify
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
            imageurl=request.get_json().get('imageurl'),
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

@app.route("/createdb", methods=['GET'])
def createdb():
    from model import db
    db.create_all()
    return "Okiely dokes"

if __name__ == "__main__":
    app.run(host='0.0.0.0')