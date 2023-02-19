import os
import sys
import yaml
from apispec import APISpec
from pathlib import Path
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from repository.tokens.active_records import TokenRepository

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from repository.cargos.active_records import CargoRepository
from repository.customers.active_records import CustomerRepository
from repository.flights.active_records import FlightRepository
from repository.registry import RepositoriesRegistry
from repository.rockets.active_records import RocketRepository
from repository.users.active_records import UserRepository
from .auth.authentication import auth_blueprint

from web.config import config_by_name


def create_app(config_name='prod'):
    app = Flask(__name__)

    app.config.from_object(config_by_name[config_name])

    altex_api = Api(app)
    db = SQLAlchemy(app)
    app.repositories = RepositoriesRegistry(cargos=CargoRepository, flights=FlightRepository, rockets=RocketRepository,
                                            customers=CustomerRepository, users=UserRepository, tokens=TokenRepository)
    app.session = db.session
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "query_string"]
    jwt = JWTManager(app)

    from .api.api import api_blueprint
    altex_api.register_blueprint(api_blueprint)
    altex_api.register_blueprint(auth_blueprint)

    return app
