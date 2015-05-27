import json
from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

from model import db, Tap, User

app = Flask(__name__)


@app.route("/user", methods=['GET', 'POST'])
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
    else:
        return ""

@app.route("/auth", methods=['POST'])
def auth():
    if request.method == 'POST':
        pass

@app.route("/tap", methods=['GET', 'POST'])
def tap():
    if request.method == 'POST':
        tap = Tap(
            page_token=request.get_json().get('page_token'),
            page_uid=request.get_json().get('page_uid'),
            element_route=request.get_json().get('element_route'),
            node=request.get_json().get('node'),
            comment=request.get_json().get('comment'),
            create_date=request.get_json().get('create_date', None),
        )
        db.session.add(tap)
        db.session.commit()
        return jsonify(tap.serialize)
    else:
        results = None
        if request.args.get('page_token'):
            results = Tap.query \
                .filter_by(page_token=request.args.get('page_token', '')) \
                .order_by(Tap.create_date) \
                .all()
        elif request.args.get('page_uid'):
            results = Tap.query \
                .filter_by(page_uid=request.args.get('page_uid', '')) \
                .order_by(Tap.create_date) \
                .all()
        return jsonify(taps=[t.serialize for t in results]) if results else ""

@app.route("/createdb", methods=['GET'])
def createdb():
    from model import db
    db.create_all()
    return "Okiely dokes"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)