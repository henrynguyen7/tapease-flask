import json
from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

from model import Annotation
from model import db

app = Flask(__name__)

@app.route("/tap", methods=['GET', 'POST'])
def tap():
    if request.method == 'POST':
        tap = Tap(
            base_url=request.get_json().get('base_url'),
            params=request.get_json().get('params'),
            element_route=request.get_json().get('element_route'),
            username=request.get_json().get('username'),
            image_url=request.get_json().get('image_url'),
            comment=request.get_json().get('comment'),
            date=request.get_json().get('date', None),
        )
        db.session.add(tap)
        db.session.commit()
        return jsonify(tap.serialize)
    else:
        results = Tap.query \
            .filter_by(base_url=request.args.get('base_url', '')) \
            .order_by(Tap.date) \
            .all()
        return jsonify(taps=[t.serialize for t in results])

@app.route("/createdb", methods=['GET'])
def createdb():
    from model import db
    db.create_all()
    return "Okiely dokes"

if __name__ == "__main__":
    app.run(host='0.0.0.0')