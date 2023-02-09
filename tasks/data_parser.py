import datetime
import logging
from typing import BinaryIO, Union, Any, Dict, List
import pandas as pd
import psycopg2
from flask import current_app, Flask, jsonify
from app_loggers.logger import LoggerObserver
from datetime import datetime
# app_ = Flask(__name__)


logger = LoggerObserver(__name__).logger
logger.setLevel(logger.level)


def read_csv_or_xls(file: Union[str, BinaryIO]) -> Dict[str, List[Dict[str, Union[str, int]]]]:
    file_extension = file.filename.rsplit(".", 1)[1] if hasattr(file, "filename") else file.rsplit(".", 1)[1]
    if file_extension not in ["csv", "xls", "xlsx"]:
        raise ValueError("Invalid file format. Only .csv and .xls/.xlsx formats are supported.")

    if file_extension in ["csv"]:
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    rockets = []
    rocket_ids = {}
    for index, row in df.iterrows():
        vehicle_type = row['Vehicle Type']
        if vehicle_type not in rocket_ids:
            rocket_id = len(rocket_ids)
            rocket_ids[vehicle_type] = rocket_id
            rockets.append({'id': rocket_id, 'vehicle_type': vehicle_type})

    customers = []
    customer_ids = {}
    for index, row in df.iterrows():
        customer_name = row['Customer Name']
        if customer_name not in customer_ids:
            customer_id = len(customer_ids)
            customer_ids[customer_name] = customer_id
            customer = {'id': customer_id, 'customer_name': customer_name, 'customer_type': row['Customer Type'],
                        'country': row['Customer Country']}
            customers.append(customer)
    logger.log(level=logging.DEBUG, msg=customer_ids)
    cargos = []
    cargo_ids = {}
    for index, row in df.iterrows():
        payload_name = row['Payload Name']
        if payload_name not in cargo_ids:
            cargo_id = len(cargo_ids)
            cargo_ids[payload_name] = cargo_id
            cargo = {'id': cargo_id, 'name': payload_name, 'payload_type': row['Payload Type'],
                     'mass': row['Payload Mass (kg)'], 'orbit': row['Payload Orbit']}
            cargos.append(cargo)

    flights = []
    for index, row in df.iterrows():
        flight = dict()
        flight['number'] = row['Flight Number']
        flight['launch_date'] = row['Launch Date']
        flight['flight_status'] = 'schedule'
        flight['launch_time'] = row['Launch Time']
        flight['launch_site'] = row['Launch Site']
        flight['mission_outcome'] = row['Mission Outcome']
        flight['failure_reason'] = row['Failure Reason']
        flight['landing_type'] = row['Landing Type']
        flight['landing_outcome'] = row['Landing Outcome']
        flight['rocket_id'] = rocket_ids[row['Vehicle Type']]
        flight['customer_id'] = customer_ids[row['Customer Name']]
        flight['cargo_id'] = cargo_ids[row['Payload Name']]
        flights.append(flight)

    result = {
        "rockets": rockets,
        "customers": customers,
        "cargos": cargos,
        "flights": flights
    }
    return result


def upload_csv_or_xls(file):
    try:
        data = read_csv_or_xls(file)
    except Exception as e:
        logger.log(level=logging.ERROR, msg=str(e))
        raise Exception('File could not be uploaded, wil try again later')

    session = current_app.session()
    try:
        session.begin()
        with session:
            customers_repo = current_app.repositories.customers_repo(session)
            rockets_repo = current_app.repositories.rockets_repo(session)
            cargos_repo = current_app.repositories.cargos_repo(session)
            flights_repo = current_app.repositories.flights_repo(session)

            for row in data['rockets']:
                try:
                    rockets_repo.add(vehicle_type=row['vehicle_type'])
                except Exception as e:
                    logger.log(level=logging.ERROR, msg=f"Error adding rocket data: {e}")

            for row in data['customers']:
                try:
                    customers_repo.add(name=row['customer_name'], customer_type=row['customer_type'], country=row['country'])
                except Exception as e:
                    logger.log(level=logging.ERROR, msg=f"Error adding customer data: {e}")

            for row in data['cargos']:
                try:
                    cargos_repo.add(name=row['name'], payload_type=row['payload_type'], mass=row['mass'],
                                    orbit=row['orbit'])
                except Exception as e:
                    logger.log(level=logging.ERROR, msg=f"Error adding cargo data: {e}")
            session.commit()
            session.begin()
            for row in data['flights']:
                try:
                    time = datetime.strptime(row['launch_time'], "%H:%M").time()
                    date = datetime.strptime(row['launch_date'], "%d %B %Y").date()


                    # Combine the date and time into a single timestamp value
                    launch_time = datetime.combine(date, time)
                    # customers = customers_repo.get_multiple([cust_id for cust_id in row['customer_id']], True)
                    # cargos = cargos_repo.get_multiple([cargo_id for cargo_id in row['cargo_id']], True)
                    flights_repo.add(
                        number=row['number'], launch_date=row['launch_date'], flight_status=row['flight_status'],
                        launch_time=launch_time, launch_site=row['launch_site'],
                        mission_outcome=row['mission_outcome'],
                        failure_reason=row['failure_reason'], landing_type=row['landing_type'],
                        landing_outcome=row['landing_outcome'])
                except psycopg2.Error as e:
                    logger.log(level=logging.ERROR, msg=f"Error adding flight data: {e}")

            session.commit()
    except Exception as e:
        logger.log(level=logging.ERROR, msg=f"Error processing the whole data: {e}")
        session.rollback()
    else:
        logger.log(level=logging.DEBUG, msg='data successfully loaded')
    finally:
        session.close()
