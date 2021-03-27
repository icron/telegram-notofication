from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from flask_login import login_user, current_user, login_required, logout_user

from app.auth.telegram import Telegram
from app.user.model import Users
from app.user.validation import validate_create_users
from app.util.util import InvalidUsage


def auth_blueprint(db, bot_token: str):
    auth = Blueprint('auth', __name__)

    @auth.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    @auth.route('/login', methods=['GET'])
    def login_get() -> str:
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        return render_template('auth/login.html')

    @auth.route('/login', methods=['POST'])
    def login() -> str:
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        errors = validate_create_users(request)
        if errors is not None:
            raise InvalidUsage(errors)

        auth_telegram = Telegram(request.json, bot_token)

        if not auth_telegram.check():
            raise InvalidUsage("auth_failed")

        user_model = Users(db)
        user = user_model.find(request.json.get('id'))

        if user is None:
            user = user_model.create(request.json)

        login_user(user)

        session.pop('_flashes', None)

        return jsonify({'code': 'ok'})

    return auth
