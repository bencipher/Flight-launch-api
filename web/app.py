import os
import sys
import yaml
import alembic.config
from apispec import APISpec
from pathlib import Path
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

from repository.tokens.active_records import TokenRepository
from .api.api import api_blueprint
from .auth.authentication import auth_blueprint

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from repository.cargos.active_records import CargoRepository
from repository.customers.active_records import CustomerRepository
from repository.flights.active_records import FlightRepository
from repository.registry import RepositoriesRegistry
from repository.rockets.active_records import RocketRepository
from repository.users.active_records import UserRepository

from web.config import config_by_name

app = Flask(__name__)

config_name = os.getenv('FLASK_ENV', 'prod')
app.config.from_object(config_by_name[config_name])

altex_api = Api(app)
db = SQLAlchemy(app)
# db.init_app(app)
altex_api.register_blueprint(api_blueprint)
altex_api.register_blueprint(auth_blueprint)

api_spec = yaml.safe_load((Path(__file__).parent / "api/oas.yaml").read_text())
spec = APISpec(
    title=api_spec["info"]["title"],
    version=api_spec["info"]["version"],
    openapi_version=api_spec["openapi"],
)
spec.to_dict = lambda: api_spec
altex_api.spec = spec
app.repositories = RepositoriesRegistry(cargos=CargoRepository, flights=FlightRepository, rockets=RocketRepository,
                                        customers=CustomerRepository, users=UserRepository, tokens=TokenRepository)
app.session = db.session
app.config["JWT_TOKEN_LOCATION"] = ["headers", "query_string"]
jwt = JWTManager(app)