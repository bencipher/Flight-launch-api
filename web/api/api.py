import logging

from flask import current_app, jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
import sys

from webargs.flaskparser import use_args

from app_loggers.logger import LoggerObserver
from tasks.data_parser import upload_csv_or_xls

sys.path.append("../utils")
from .schemas import (CargoSchema, FlightSchema, RocketSchema, CustomerSchema, GetCustomerSchema,
                      GetFlightSchema, GetRocketSchema, GetCargoSchema, GetUserSchema, QueryFlightSchema, UserSchema,
                      UploadCSVorXLSArgs, UpdateUserSchema)

api_blueprint = Blueprint("api", __name__, description="Altex API")

logger = LoggerObserver(__name__).logger
logger.setLevel(logger.level)


@api_blueprint.route("/api/users")
class Users(MethodView):
    
    @api_blueprint.response(status_code=200, schema=GetUserSchema(many=True))
    def get(self):
        try:
            session = current_app.session()
            with session:
                users_repo = current_app.repositories.users_repo(session)
                users = users_repo.list()
                return users
        except Exception as e:
            return jsonify(error=str(e)), 404

    
    @api_blueprint.arguments(UserSchema(partial=False))
    @api_blueprint.response(status_code=201, schema=GetUserSchema)
    def post(self, payload):
        session = current_app.session()
        try:
            users_repo = current_app.repositories.users_repo(session)
            user = users_repo.add(payload)
            logger.log(level=logging.DEBUG, msg=user)
            session.commit()
            return user
        except Exception as e:
            logger.log(level=logging.ERROR, msg=str(e))
            return jsonify(error=str(e)), 400


@api_blueprint.route("/api/users/<user_id>")
class User(MethodView):
    
    @api_blueprint.response(status_code=200, schema=GetUserSchema)
    def get(self, user_id):
        session = current_app.session()
        try:
            with session:
                users_repo = current_app.repositories.users_repo(session)
                user = users_repo.get(user_id)
                return user
        except Exception as e:
            return jsonify(error=str(e)), 400

    
    @api_blueprint.arguments(UpdateUserSchema)
    @api_blueprint.response(status_code=200, schema=GetUserSchema)
    def put(self, payload, user_id):
        try:
            session = current_app.session()
            with session:
                users_repo = current_app.repositories.users_repo(session)
                user = users_repo.update(user_id, **payload)
                session.commit()
                return user
        except Exception as e:
            return jsonify(error=str(e)), 400

    
    @api_blueprint.response(status_code=204)
    def delete(self, user_id):
        try:
            session = current_app.session()
            with session:
                users_repo = current_app.repositories.users_repo(session)
                users_repo.delete(user_id)
                session.commit()
        except Exception as e:
            return jsonify(error=str(e)), 400


@api_blueprint.route("/api/rockets")
class Rockets(MethodView):

    
    @api_blueprint.response(status_code=200, schema=GetRocketSchema(many=True))
    def get(self):
        try:
            session = current_app.session()
            with session:
                rockets_repo = current_app.repositories.rockets_repo(session)
                rockets = rockets_repo.list()
                return rockets
        except Exception as e:
            return jsonify(error=str(e)), 500

    
    @api_blueprint.arguments(RocketSchema)
    @api_blueprint.response(status_code=201, schema=GetRocketSchema)
    def post(self, payload):
        session = current_app.session()
        try:
            rocket_repo = current_app.repositories.rockets_repo(s)
            rocket = rocket_repo.add(**payload)
            session.commit()
            return rocket
        except Exception as e:
            logger.log(level=logging.ERROR, msg=str(e))
            return jsonify(error=str(e)), 400


@api_blueprint.route("/api/rockets/<rocket_id>")
class Rocket(MethodView):

    
    @api_blueprint.response(status_code=200, schema=GetRocketSchema)
    def get(self, rocket_id):
        session = current_app.session()
        try:
            with session:
                rocket_repo = current_app.repositories.rockets_repo(session)
                rocket = rocket_repo.get(rocket_id)
                return rocket
        except Exception as e:
            logger.log(level=logging.ERROR, msg=str(e))
            return jsonify(error=str(e)), 404

    
    @api_blueprint.arguments(RocketSchema)
    @api_blueprint.response(status_code=200, schema=GetRocketSchema)
    def put(self, payload, rocket_id):
        try:
            session = current_app.session()
            with session:
                rockets_repo = current_app.repositories.rockets_repo(session)
                rocket = rockets_repo.update(rocket_id, **payload)
                session.commit()
                return rocket
        except Exception as e:
            return jsonify(error=str(e)), 400

    
    @api_blueprint.response(status_code=204)
    def delete(self, rocket_id):
        try:
            session = current_app.session()
            with session:
                rockets_repo = current_app.repositories.rockets_repo(session)
                rockets_repo.delete(rocket_id)
                session.commit()
        except Exception as e:
            return jsonify(error=str(e)), 400


@api_blueprint.route("/api/customers")
class Customers(MethodView):
    
    @api_blueprint.response(status_code=200, schema=GetCustomerSchema(many=True))
    def get(self):
        try:
            session = current_app.session()
            with session:
                customers_repo = current_app.repositories.customers_repo(session)
                customers = customers_repo.list()
                return customers
        except Exception as e:
            return jsonify(error=str(e)), 500

    
    @api_blueprint.arguments(CustomerSchema)
    @api_blueprint.response(status_code=201, schema=GetCustomerSchema)
    def post(self, payload):
        session = current_app.session()
        try:
            customers_repo = current_app.repositories.customers_repo(s)
            customer = customers_repo.add(**payload)
            session.commit()
            return customer
        except Exception as e:
            logger.log(level=logging.ERROR, msg=str(e))
            return jsonify(error=str(e)), 400


@api_blueprint.route("/api/rockets/<customer_id>")
class Customer(MethodView):
    
    @api_blueprint.response(status_code=200, schema=GetCustomerSchema)
    def get(self, customer_id):
        session = current_app.session()
        try:
            with session:
                customers_repo = current_app.repositories.customers_repo(session)
                customer = customers_repo.get(customer_id)
                return customer
        except Exception as e:
            logger.log(level=logging.ERROR, msg=str(e))
            return jsonify(error=str(e)), 404

    
    @api_blueprint.arguments(CustomerSchema)
    @api_blueprint.response(status_code=200, schema=GetCustomerSchema)
    def put(self, payload, customer_id):
        try:
            session = current_app.session()
            with session:
                customers_repo = current_app.repositories.customers_repo(session)
                customer = customers_repo.update(customer_id, **payload)
                session.commit()
                return customer
        except Exception as e:
            return jsonify(error=str(e)), 400

    
    @api_blueprint.response(status_code=204)
    def delete(self, customer_id):
        try:
            session = current_app.session()
            with session:
                customers_repo = current_app.repositories.customers_repo(session)
                customers_repo.delete(customer_id)
                session.commit()
        except Exception as e:
            return jsonify(error=str(e)), 400


@api_blueprint.route("/api/flights/<flight_id>")
class Flight(MethodView):

    # @blueprint.arguments(QueryFlightSchema, location="query")
    
    @api_blueprint.response(status_code=200, schema=GetFlightSchema)
    def get(self, flight_id):
        session = current_app.session()
        try:
            with session:
                flight_repo = current_app.repositories.flights_repo(session)
                flight = flight_repo.get(flight_id)
                return flight
        except Exception as e:
            logger.log(level=logging.ERROR, msg=str(e))
            return jsonify(error=str(e)), 404

    
    @api_blueprint.arguments(FlightSchema)
    @api_blueprint.response(status_code=200, schema=GetFlightSchema)
    def put(self, payload, flight_id):
        rocket_id = payload['rocket_id']
        customer_id = payload['customer_id']
        cargo_ids = payload['cargo_id']

        try:
            session = current_app.session()
            with session:
                _, customers, cargos = _validate_flight_extras(session, rocket_id, customer_id, cargo_ids)
                payload['customer_id'] = customers
                payload['cargo_id'] = cargos
                flight_repo = current_app.repositories.flights_repo(session)
                flight = flight_repo.update(flight_id, **payload)
                session.commit()
                return flight
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': 'An unexpected error has occurred'}, 500

    
    @api_blueprint.response(status_code=204)
    def delete(self, flight_id):
        try:
            session = current_app.session()
            with session:
                flight_repo = current_app.repositories.flights_repo(session)
                flight_repo.delete(flight_id)
                session.commit()
        except Exception as e:
            return jsonify(error=str(e)), 400


@api_blueprint.route("/api/flights")
class Flights(MethodView):

    
    @api_blueprint.response(status_code=200, schema=GetFlightSchema(many=True))
    def get(self):
        session = current_app.session()
        try:
            with session:
                flight_repo = current_app.repositories.flights_repo(session)
                flights = flight_repo.list()
                return flights
        except Exception as e:
            logger.log(level=logging.ERROR, msg=str(e))
            return jsonify(error=str(e)), 404

    
    @api_blueprint.arguments(FlightSchema)
    @api_blueprint.response(status_code=201, schema=GetFlightSchema)
    def post(self, payload):
        rocket_id = payload['rocket_id']
        customer_ids = payload['customer_id']
        cargo_ids = payload['cargo_id']

        try:
            session = current_app.session()
            _, customers, cargos = _validate_flight_extras(session, rocket_id, customer_ids, cargo_ids)
            payload['customer_id'] = customers
            payload['cargo_id'] = cargos
            flight_repo = current_app.repositories.flights_repo(session)
            flight = flight_repo.add(**payload)
            session.commit()
            return flight

        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            current_app.logger.exception(e)
            return {'message': 'An unexpected error has occurred'}, 500


@api_blueprint.route("/api/cargos/<cargo_id>")
class Cargo(MethodView):

    
    @api_blueprint.response(status_code=200, schema=GetCargoSchema)
    def get(self, cargo_id):
        session = current_app.session()
        try:
            with session:
                cargos_repo = current_app.repositories.cargos_repo(session)
                cargo = cargos_repo.get(cargo_id)
                return cargo
        except Exception as e:
            logger.log(level=logging.ERROR, msg=str(e))
            return jsonify(error=str(e)), 404

    
    @api_blueprint.arguments(CargoSchema)
    @api_blueprint.response(status_code=200, schema=GetCargoSchema)
    def put(self, payload, cargo_id):
        try:
            session = current_app.session()
            with session:
                cargos_repo = current_app.repositories.cargos_repo(session)
                cargo = cargos_repo.update(cargo_id, **payload)
                session.commit()
                return cargo
        except Exception as e:
            return jsonify(error=str(e)), 400

    
    @api_blueprint.response(status_code=204)
    def delete(self, cargo_id):
        try:
            session = current_app.session()
            with session:
                cargos_repo = current_app.repositories.cargos_repo(session)
                cargos_repo.delete(cargo_id)
                session.commit()
        except Exception as e:
            return jsonify(error=str(e)), 400


@api_blueprint.route("/api/cargos")
class Cargos(MethodView):

    
    @api_blueprint.response(status_code=200, schema=GetCargoSchema(many=True))
    def get(self):
        try:
            session = current_app.session()
            with session:
                cargos_repo = current_app.repositories.cargos_repo(session)
                cargos = cargos_repo.list()
                return cargos
        except Exception as e:
            return jsonify(error=str(e)), 500

    
    @api_blueprint.arguments(CargoSchema)
    @api_blueprint.response(status_code=201, schema=GetCargoSchema)
    def post(self, payload):
        session = current_app.session()
        try:
            with session as s:
                cargos_repo = current_app.repositories.cargos_repo(s)
                cargo = cargos_repo.add(**payload)
                return cargo
        except Exception as e:
            logger.log(level=logging.ERROR, msg=str(e))
            return jsonify(error=str(e)), 400


def _validate_flight_extras(session, rocket_id, customer_ids, cargo_ids):
    rockets_repo = current_app.repositories.rockets_repo(session)
    rocket = rockets_repo.get(rocket_id)
    if not rocket:
        raise ValueError(f"Rocket with id {rocket_id} doesn't exist")

    customers_repo = current_app.repositories.customers_repo(session)
    customers = customers_repo.get_multiple(customer_ids, True)
    if len(customers) != len(customer_ids):
        missing_customers = set(customer_ids) - set(c.id for c in customers)
        raise ValueError(f"Customers with ids {missing_customers} don't exist")

    cargos_repo = current_app.repositories.cargos_repo(session)
    cargos = cargos_repo.get_multiple(cargo_ids, True)
    if len(cargos) != len(cargo_ids):
        missing_cargos = set(cargo_ids) - set(c.id for c in cargos)
        raise ValueError(f"Cargos with ids {missing_cargos} don't exist")
    return rocket, customers, cargos

@api_blueprint.route('/api/upload_csv_or_xls', methods=['POST'])
@use_args(UploadCSVorXLSArgs(), location='files')
def upload_logs(args):
    file = request.files['file']
    sheet_index = args['sheet_index']
    header_row = args['header_row']
    should_preview = args['should_preview']
    upload_csv_or_xls(file)
    # Add your implementation to process the file here
    return {'message': 'File queued for batch processing'}, 200