import logging

from psycopg2._psycopg import OperationalError

from app_loggers.logger import LoggerObserver
from services.objects import Token
from repository.repository import BaseRepository
from repository.models import JwtTokenModel

logger = LoggerObserver(__name__).logger
logger.setLevel(logger.level)


class TokenRepository(BaseRepository):

    def add(self, items):
        try:
            print(f'got here with    {items}')
            token = JwtTokenModel(**items)
            self.session.add(token)
        except Exception as e:
            logger.log(level=logging.ERROR, msg=f'Error adding token with payload {items}: {e}')
            raise Exception(f'Error adding token: {e}')
        return Token(**token.as_dict(), token_record=token)

    def get(self, **filters):
        pass

    def list(self, limit=None, **filters):
        token = self.session.query(JwtTokenModel).filter_by(**filters).first()
        print(token.as_dict())
        if token:
            return token
        raise ValueError('Invalid Refresh token supplied')


    def update(self, id_, **payload):
        pass

    def delete(self, id_):
        token = self._get(id_)
        self.session.delete(token)
        self.session.commit()

    def _get(self, id_):
        try:
            return self.session.query(JwtTokenModel).filter_by(id=id_).first()
        except OperationalError as e:
            logger.log(level=logging.ERROR, msg=str(e))
            raise Exception('Problem fetching record from database')
