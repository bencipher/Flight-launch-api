import logging

from psycopg2._psycopg import OperationalError

from app_loggers.logger import LoggerObserver
from services.objects import Customer
from repository.models import CustomerModel
from repository.repository import BaseRepository

logger = LoggerObserver(__name__).logger
logger.setLevel(logger.level)


class CustomerRepository(BaseRepository):

    def _get(self, id_):
        try:
            return self.session.query(CustomerModel).filter_by(id=id_).first()
        except OperationalError as e:
            logger.log(level=logging.ERROR, msg=str(e))
            raise Exception('Problem fetching Customer record from database')

    def get(self, id_=None):
        # not EAFP COMPLIANT BUT STILL WORK REGARDLESS
        customer = self._get(id_)
        if customer:
            return Customer(**customer.as_dict())
        else:
            raise Exception(f"Rocket with id '{id_}' not found")

    def add(self, **items):
        try:
            customer = CustomerModel(**items)
            self.session.add(customer)

        except Exception as e:
            logger.log(level=logging.ERROR, msg=f'Error adding customer with payload {items}: {e}')
            raise Exception(f'Error adding rocket: {e}')
        return Customer(**customer.as_dict(), customer_record=customer)

    def list(self, limit=None, **filters):
        try:
            customers = self.session.query(CustomerModel).filter_by(**filters).limit(limit).all()
        except Exception as e:
            logger.log(level=logging.ERROR, msg=f'Error listing customer: {e}')
            raise Exception(f'Error listing rockets: {e}')
        return [Customer(**customer.as_dict()) for customer in customers]

    def update(self, id_, **payload):

        customer = self._get(id_)
        if not customer:
            raise Exception(f"Customer with id '{id_}' not found")
        self.session.merge(customer)
        try:
            for key, value in payload.items():
                setattr(customer, key, value)
        except Exception as e:
            logger.log(level=logging.ERROR, msg=f'Error updating customer with id {id_} and payload {payload}: {e}')
            raise Exception(f'Error updating customer: {e}')
        return Customer(**customer.as_dict())

    def delete(self, id_):
        customer = self._get(id_)
        if not customer:
            raise Exception("Customer not found.")
        try:
            self.session.delete(customer)
        except Exception as e:
            logger.error(f'Error occurred while deleting customer: {e}')
            raise Exception('Error occurred while deleting customer.')

    def get_multiple(self, ids, db_object=False):
        customers = self.session.query(CustomerModel).filter(CustomerModel.id.in_(ids)).all()
        return customers if db_object else [Customer(**customer.as_dict()) for customer in customers]
