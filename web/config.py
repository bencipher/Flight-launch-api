# from decouple import Config, RepositoryEnv

# Create a Config object
# config = Config(RepositoryEnv('../.env'))
import os


class BaseConfig:
    debug = False
    API_TITLE = 'ALTEX API'
    API_VERSION = 'v1'
    OPENAPI_VERSION = '3.0.3'
    OPENAPI_JSON_PATH = 'openapi/altex.json'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_REDOC_PATH = '/redoc'
    OPENAPI_REDOC_URL = 'https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js'  # noqa: E501
    OPENAPI_SWAGGER_UI_PATH = '/'
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Production(BaseConfig):
    debug = False


class Development(BaseConfig):
    debug = True


config_by_name = dict(
    development=Development,
    prod=Production
)
