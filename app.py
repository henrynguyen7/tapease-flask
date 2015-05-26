import json
from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

from model import Annotation
from model import db

app = Flask(__name__)


@app.route("/user", methods=['POST'])
def user():
    if request.method == 'POST':
        user = User(
            email=request.get_json().get('email'),
            password=request.get_json().get('password'),
            name=request.get_json().get('name'),
            image_url=request.get_json().get('image_url'),
        )
        db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize)

@app.route("/auth", methods=['POST'])
def auth():
    if request.method == 'POST':
        pass

@app.route("/tap", methods=['GET', 'POST'])
def tap():
    if request.method == 'POST':
        tap = Tap(
            user_id=request.get_json().get('user_id'),
            page_token=request.get_json().get('page_token'),
            base_url=request.get_json().get('base_url'),
            route_params=request.get_json().get('route_params'),
            query_params=request.get_json().get('query_params'),
            element_route=request.get_json().get('element_route'),
            node=request.get_json().get('node'),
            comment=request.get_json().get('comment'),
            create_date=request.get_json().get('create_date', None),
        )
        db.session.add(tap)
        db.session.commit()
        return jsonify(tap.serialize)
    else:
        if request.args.get('page_token'):
            results = Tap.query \
                .filter_by(page_token=request.args.get('page_token', '')) \
                .order_by(Tap.create_date) \
                .all()
        elif request.args.get('base_url'):
            results = Tap.query \
                .filter_by(base_url=request.args.get('base_url', '')) \
                .order_by(Tap.create_date) \
                .all()
        return jsonify(taps=[t.serialize for t in results])

@app.route("/createdb", methods=['GET'])
def createdb():
    from model import db
    db.create_all()
    return "Okiely dokes"

if __name__ == "__main__":
    app.run(host='0.0.0.0')