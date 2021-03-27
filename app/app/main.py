from os import environ

import boto3
from flask import Flask, jsonify, session, render_template
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_required, user_logged_out

from app.auth.api import auth_blueprint
from app.keywords.api import keywords_blueprint
from app.session import Session
from app.user.model import Users
from app.util.util import InvalidUsage

app = Flask(__name__)
app.logger
app.config['SESSION_DYNAMODB_TABLE'] = str(environ.get("SESSION_DYNAMODB_TABLE", None))
app.config['SESSION_DYNAMODB_REGION'] = str(environ.get("SESSION_DYNAMODB_REGION", None))
app.config['SESSION_COOKIE_HTTPONLY'] = str(environ.get("SESSION_COOKIE_HTTPONLY", None))
app.config['SECRET_KEY'] = str(environ.get("SECRET_KEY", None))
Session(app)
Bootstrap(app)

port = int(environ.get("PORT", 5000))
debug = bool(environ.get("DEBUG", False))
telegram_bot_token = str(environ.get("TELEGRAM_BOT_TOKEN", ""))

dynamoDb = boto3.resource('dynamodb')
app.register_blueprint(keywords_blueprint(dynamoDb), url_prefix='/keyword')
app.register_blueprint(auth_blueprint(dynamoDb, telegram_bot_token), url_prefix='/auth')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.user_loader(Users(dynamoDb).find)
login_manager.init_app(app)


@user_logged_out.connect_via(app)
def user_logged_out(app, user):
    session.clear()


@app.route('/k8s')
def k8s():
    return ''


@app.route('/')
@login_required
def index():
    return render_template('index/index.html')


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=debug, port=port)
