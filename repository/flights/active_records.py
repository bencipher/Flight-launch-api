import logging

from psycopg2._psycopg import OperationalError

from app_loggers.logger import LoggerObserver
from services.objects import Flight
from repository.models import FlightModel, CustomerModel
from repository.repository import BaseRepository

logger = LoggerObserver(__name__).logger
logger.setLevel(logger.level)


class FlightRepository(BaseRepository):

    def _get(self, id):
        try:
            return self.session.query(FlightModel).filter_by(id=id).first()
        except OperationalError as e:
            logger.log(level=logging.ERROR, msg=str(e))
            raise Exception('Problem fetching Flight record from database')

    def get(self, id_=None):
        flight = self._get(id_)
        if flight:
            return Flight(**flight.as_dict())
        else:
            raise Exception(f"Flight with id '{id_}' not found")

    def add(self, **items):
        try:
            flight = FlightModel(**items)
            self.session.add(flight)
        except Exception as e:
            logger.log(level=logging.ERROR, msg=f'Error adding flight with payload {items}: {e}')
            raise Exception(f'Error adding flight: {e}')
        logger.log(level=logging.DEBUG, msg=f' flight with payload {flight} loaded successfully')
        return Flight(**flight.as_dict(), flight_record=flight)

    def list(self, limit=None, **filters):
        logger.log(level=logging.DEBUG, msg='in flight list function')
        try:
            flights = self.session.query(FlightModel).filter_by(**filters).limit(limit).all()
        except Exception as e:
            logger.log(level=logging.ERROR, msg=f'Error listing flights: {e}')
            raise Exception(f'Error listing flights: {e}')

        return [Flight(**flight.as_dict()) for flight in flights]

    def update(self, id_, **payload):
        flight = self._get(id_)
        if not flight:
            raise Exception(f"Flight with id '{id_}' not found")
        self.session.merge(flight)
        try:
            for key, value in payload.items():
                setattr(flight, key, value)
        except Exception as e:
            logger.log(level=logging.ERROR, msg=f'Error updating flight with id {id_} and payload {payload}: {e}')
            raise Exception(f'Error updating flight: {e}')
        return Flight(**flight.as_dict())

    def delete(self, id_):
        flight = self._get(id_)
        if flight:
            try:
                self.session.delete(flight)
            except Exception as e:
                logger.error(f'Error occurred while deleting flight: {e}')
                raise Exception('Error occurred while deleting flight.')
        else:
            raise Exception("Flight not found.")
