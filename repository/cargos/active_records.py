import logging

from psycopg2._psycopg import OperationalError

from app_loggers.logger import LoggerObserver
from services.objects import Cargo
from repository.repository import BaseRepository
from repository.models import CargoModel

logger = LoggerObserver(__name__).logger
logger.setLevel(logger.level)


class CargoRepository(BaseRepository):

    def _get(self, id):
        try:
            return self.session.query(CargoModel).filter_by(id=id).first()
        except OperationalError as e:
            logger.log(level=logging.ERROR, msg=str(e))
            raise Exception('Problem fetching Cargo record from database')

    def get(self, id_=None):
        cargo = self._get(id_)
        if cargo:
            return Cargo(**cargo.as_dict())
        else:
            raise Exception(f"Cargo with id '{id_}' not found")

    def add(self, **items):
        try:
            cargo = CargoModel(**items)
            self.session.add(cargo)
        except Exception as e:
            logger.log(level=logging.ERROR, msg=f'Error adding cargo with payload {items}: {e}')
            raise Exception(f'Error adding rocket: {e}')
        return Cargo(**cargo.as_dict(), cargo_record=cargo)

    def list(self, limit=None, **filters):
        try:
            cargos = self.session.query(CargoModel).filter_by(**filters).limit(limit).all()
        except Exception as e:
            logger.log(level=logging.ERROR, msg=f'Error listing cargos: {e}')
            raise Exception(f'Error listing cargos: {e}')
        return [Cargo(**cargo.as_dict()) for cargo in cargos]

    def update(self, id_, **payload):
        cargo = self._get(id_)
        if not cargo:
            raise Exception(f"Cargo with id '{id_}' not found")
        self.session.merge(cargo)
        try:
            for key, value in payload.items():
                setattr(cargo, key, value)
        except Exception as e:
            logger.log(level=logging.ERROR, msg=f'Error updating cargo with id {id_} and payload {payload}: {e}')
            raise Exception(f'Error updating cargo: {e}')
        return Cargo(**cargo.as_dict())

    def delete(self, id_):
        cargo = self._get(id_)
        if not cargo:
            raise Exception('Cargo not found')
        try:
            self.session.delete(cargo)
        except Exception as e:
            logger.error(f'Error occurred while deleting cargo: {e}')
            raise Exception('Error occurred while deleting cargo.')

    def get_multiple(self, ids, db_object=False):
        cargos = self.session.query(CargoModel).filter(CargoModel.id.in_(ids)).all()
        return cargos if db_object else [Cargo(**cargo.as_dict()) for cargo in cargos]
