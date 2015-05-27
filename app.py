#!/usr/bin/env python

import json
from flask import Flask, request, jsonify
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.sqlalchemy import SQLAlchemy

from model import db, User, Tap

app = Flask(__name__)
auth = HTTPBasicAuth()


@app.route('/user', methods = ['POST'])
def create_user():
    email = request.json.get('email')
    password = request.json.get('password')
    name = request.json.get('name')
    image_url = request.json.get('image_url')
    is_enabled = request.json.get('is_enabled')
    if email is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(email=email).first() is not None:
        abort(400) # existing user
    user = User(
        email=email,
        password=password,
        name=name,
        image_url=image_url,
        is_enabled=is_enabled
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize)


@app.route('/user', methods = ['PUT'])
@auth.login_required
def update_user():
    # TODO: Check if auth'd, then allow update
    pass


@app.route("/auth", methods=['POST'])
@auth.login_required
def auth():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route("/tap", methods=['POST'])
@auth.login_required
def create_tap():
    tap = Tap(
        page_token=request.get_json().get('page_token'),
        page_uid=request.get_json().get('page_uid'),
        element_route=request.get_json().get('element_route'),
        node=request.get_json().get('node'),
        comment=request.get_json().get('comment'),
    )
    db.session.add(tap)
    db.session.commit()
    return jsonify(tap.serialize)


@app.route("/tap", methods=['GET'])
@auth.login_required
def get_tap():
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


@auth.verify_password
def verify_password(email_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(email_or_token)
    if not user:
        # try to authenticate with email/password
        user = User.query.filter_by(email=email_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


if __name__ == "__main__":
    if not os.path.exists('tapeasedb.sqlite'):
        db.create_all()
    app.run(host='0.0.0.0', debug=True)