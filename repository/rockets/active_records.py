import logging

from psycopg2._psycopg import OperationalError

from app_loggers.logger import LoggerObserver
from services.objects import Rocket
from repository.models import RocketModel
from repository.repository import BaseRepository

logger = LoggerObserver(__name__).logger
logger.setLevel(logger.level)


class RocketRepository(BaseRepository):
    def _get(self, id):
        try:
            return self.session.query(RocketModel).filter_by(id=id).first()
        except OperationalError as e:
            logger.log(level=logging.ERROR, msg=str(e))
            raise Exception('Problem fetching Rocket record from database')

    def get(self, id_=None):
        rocket = self._get(id_)
        if rocket:
            return Rocket(**rocket.as_dict())
        else:
            raise ValueError(f"Rocket with id '{id_}' not found")

    def add(self, **items):
        try:
            rocket = RocketModel(**items)
            self.session.add(rocket)
        except Exception as e:
            logger.log(level=logging.ERROR, msg=f'Error adding rocket with payload {items}: {e}')
            raise Exception(f'Error adding rocket: {e}')
        return Rocket(**rocket.as_dict(), rocket_record=rocket)

    def list(self, limit=None, **filters):
        try:
            rockets = self.session.query(RocketModel).filter_by(**filters).limit(limit).all()
        except Exception as e:
            logger.log(level=logging.ERROR, msg=f'Error listing rockets: {e}')
            raise Exception(f'Error listing rockets: {e}')

        return [Rocket(**rocket.as_dict()) for rocket in rockets]

    def update(self, id_, **payload):
        rocket = self._get(id_)
        if not rocket:
            raise Exception(f"Rocket with id '{id_}' not found")
        self.session.merge(rocket)
        try:
            for key, value in payload.items():
                setattr(rocket, key, value)
        except Exception as e:
            logger.log(level=logging.ERROR, msg=f'Error updating rocket with id {id_} and payload {payload}: {e}')
            raise Exception(f'Error updating rocket: {e}')
        return Rocket(**rocket.as_dict())

    def delete(self, id_):
        rocket = self._get(id_)
        if rocket:
            try:
                self.session.delete(rocket)
            except Exception as e:
                logger.error(f'Error occurred while deleting rocket: {e}')
                raise Exception('Error occurred while deleting rocket.')
        else:
            raise Exception("Rocket not found.")
