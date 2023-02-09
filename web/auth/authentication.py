import logging
import os
import secrets
from datetime import datetime, timedelta

import jwt
from flask import current_app, jsonify, Flask
from flask.views import MethodView
from flask_smorest import Blueprint

from app_loggers.logger import LoggerObserver

from web.api.schemas import TokenSchema, RefreshTokenSchema, LoginSchema

app_ = Flask(__name__)

app_.config['SECRET_KEY'] = os.environ.get('APP_SECRET')

auth_blueprint = Blueprint("auth_api", __name__, description="Altex API Auths")

logger = LoggerObserver(__name__).logger
logger.setLevel(logger.level)


@auth_blueprint.route('/login')
class Login(MethodView):
    @auth_blueprint.arguments(LoginSchema)
    @auth_blueprint.response(schema=TokenSchema, status_code=200)
    @auth_blueprint.response(400, 'Bad Request')
    @auth_blueprint.response(401, 'Unauthorized')
    def post(self, payload):
        try:
            session = current_app.session()
            with session:
                users_repo = current_app.repositories.users_repo(session)
                tokens_repo = current_app.repositories.tokens_repo(session)
                user = users_repo.get_by_username(payload['username'])
                logger.log(level=logging.ERROR, msg=f'got {user.as_dict()}')
                if not user.check_password(payload['password']):
                    raise ValueError('Username or Password incorrect')
                access_token = jwt.encode({
                    'user_id': user.id,
                    'exp': datetime.utcnow() + timedelta(minutes=30)
                }, app_.config['SECRET_KEY'], algorithm="HS256")
                logger.log(level=40, msg='got here')
                refresh_token = secrets.token_hex(16)
                tokens_repo.add({'user_id': user.id, 'refresh_token': refresh_token})

                return jsonify({
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }), 200

        except Exception as e:
            logger.log(level=logging.ERROR, msg=str(e))
            return jsonify(error='Invalid username or password'), 401


@auth_blueprint.route('/logout')
class Logout(MethodView):
    @auth_blueprint.arguments(RefreshTokenSchema)
    @auth_blueprint.response(204, 'Success')
    @auth_blueprint.response(401, 'Unauthorized')
    def post(self, payload):
        session = current_app.session()
        with session:
            tokens_repo = current_app.repositories.tokens_repo(session)
            token = tokens_repo.list(refresh_token=payload['refresh_token'])
            tokens_repo.delete(token.id)
            if not token:
                return jsonify(error='Token not found'), 401
        return jsonify(message='Logout successful'), 204


@auth_blueprint.route('/refresh')
class RefreshToken(MethodView):
    @auth_blueprint.arguments(RefreshTokenSchema)
    @auth_blueprint.response(schema=TokenSchema, status_code=200)
    @auth_blueprint.response(401, 'Unauthorized')
    def post(self, payload):
        session = current_app.session()
        with session:
            tokens_repo = current_app.repositories.tokens_repo(session)
            token = tokens_repo.list(refresh_token=payload['refresh_token'])
            if not token:
                return jsonify(error='Token not found'), 401

        access_token = jwt.encode({
            'user_id': token.user_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, app_.config['SECRET_KEY'])
        return jsonify(access_token), 200


from functools import wraps
import jwt
from flask import request, jsonify



def authenticate_jwt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            if access_token:
                access_token = access_token.split(' ')[1]
            else:
                raise ValueError('Access token not provided')

            decoded = jwt.decode(access_token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = decoded.get('user_id')
            if not user_id:
                raise ValueError('Access token is invalid')

            return func(*args, **kwargs)

        except Exception as e:
            return jsonify(error=str(e)), 401

    return wrapper
