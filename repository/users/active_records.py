import psycopg2
from psycopg2._psycopg import OperationalError

from app_loggers.logger import LoggerObserver
from repository.models import UserModel
from repository.repository import BaseRepository
from services.objects import User
import logging
import bcrypt

logger = LoggerObserver(__name__).logger
logger.setLevel(logger.level)


class UserRepository(BaseRepository):
    def _get(self, id):
        try:
            return self.session.query(UserModel).filter_by(id=id).first()
        except OperationalError as e:
            logger.log(level=logging.ERROR, msg=str(e))
            raise Exception('Problem fetching record from database')

    def get(self, id_=None):
        user = self._get(id_)
        if user:
            return User(**user.as_dict())
        else:
            raise Exception(f"User with id '{id_}' not found")

    def get_by_username(self, username):
        try:
            return self.session.query(UserModel).filter_by(username=username).first()
        except OperationalError as e:
            logger.log(level=logging.ERROR, msg=str(e))
            raise Exception('Problem fetching record from database')
        # finally:
        #     if not user or not user.check_password(items['password']):
        #         raise ValueError('Username or Password incorrect')
        #     return User(**user.as_dict())

    def add(self, items):
        logger.log(level=logging.DEBUG, msg=f'in user add function with payload {items}')
        existing_username = self.session.query(UserModel).filter_by(username=items["username"]).first()
        existing_email = self.session.query(UserModel).filter_by(email=items["email"]).first()
        if existing_email:
            logger.log(level=logging.ERROR, msg=f"User with email '{items['email']}' already exists")
            raise Exception(f"User with email '{items['email']}' already exists")
        if existing_username:
            logger.log(level=logging.ERROR, msg=f"User with username '{items['username']}' already exists")
            raise Exception(f"User with username '{items['username']}' already exists")
        # hashed_password = pbkdf2_sha256.hash(items.get('password'))
        password = items.get('password').encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        items['password'] = str(hashed_password, 'utf-8')
        print(hashed_password)
        try:
            user = UserModel(**items)
            logger.log(level=logging.DEBUG, msg=f'in user added is {user}')
            self.session.add(user)
        except Exception as e:
            logger.log(level=logging.ERROR, msg=f'Error adding user with payload {items}: {e}')
            raise Exception(f'Error adding user: {e}')
        return User(**user.as_dict(), user_record=user)

    def list(self, limit=None, **filters):
        logger.log(level=logging.DEBUG, msg='in user list function')
        try:
            users = self.session.query(UserModel).filter_by(**filters).limit(limit).all()
        except Exception as e:
            logger.log(level=logging.ERROR, msg=f'Error listing users: {e}')
            raise Exception(f'Error listing users: {e}')

        return [User(**user.as_dict()) for user in users]

    def update(self, id_, **payload):
        user = self._get(id_)
        del payload['password']
        if not user:
            raise Exception(f"User with id '{id_}' not found")
        self.session.merge(user)
        try:
            for key, value in payload.items():
                setattr(user, key, value)
        except Exception as e:
            logger.log(level=logging.ERROR, msg=f'Error updating user with id {id_} and payload {payload}: {e}')
            raise Exception(f'Error updating user: {e}')
        return User(**user.as_dict())

    def delete(self, id_):
        user = self._get(id_)
        if user:
            try:
                self.session.delete(user)
            except Exception as e:
                logger.error(f'Error occurred while deleting user: {e}')
                raise Exception('Error occurred while deleting user.')
        else:
            raise Exception("User not found.")
