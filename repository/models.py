import logging

import bcrypt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, func
from sqlalchemy.orm import relationship

from app_loggers.logger import LoggerObserver

logger = LoggerObserver(__name__).logger
logger.setLevel(logger.level)

Base = declarative_base()


class FlightModel(Base):
    __tablename__ = 'flights'
    id = Column(Integer, primary_key=True)
    number = Column(String(150), nullable=False)
    launch_date = Column(DateTime, nullable=False)
    flight_status = Column(String(150), nullable=False)
    launch_time = Column(DateTime, nullable=False)
    launch_site = Column(String(150), nullable=False)
    mission_outcome = Column(String(150), nullable=False)
    failure_reason = Column(String(150), nullable=False)
    landing_type = Column(String(150), nullable=False)
    landing_outcome = Column(String(150), nullable=False)
    # rocket_id = Column(Integer, ForeignKey("rockets.id"), nullable=True)

    # rockets = relationship("RocketModel", back_populates="flights")
    # customers = relationship("CustomerModel", secondary="flight_customers", back_populates="flights")
    # cargos = relationship("CargoModel", secondary="flight_cargos", back_populates="flights")

    def __repr__(self):
        return '<Flight {}>'.format(self.id)

    def __str__(self):
        return 'Flight: {} ({})'.format(self.number, self.launch_date)

    def as_dict(self):
        return {
            'flight_id': self.id,
            'number': self.number,
            'launch_date': self.launch_date,
            'flight_status': self.flight_status,
            'launch_time': self.launch_time,
            'launch_site': self.launch_site,
            'mission_outcome': self.mission_outcome,
            'failure_reason': self.failure_reason,
            'landing_type': self.landing_type,
            'landing_outcome': self.landing_outcome,
            # 'rocket_id': self.rocket_id
        }


class RocketModel(Base):
    __tablename__ = 'rockets'

    id = Column(Integer, primary_key=True)
    vehicle_type = Column(String(120), nullable=False)
    # flights = relationship("FlightModel", back_populates="rockets")

    def __repr__(self):
        return '<Rocket {}>'.format(self.id)

    def __str__(self):
        return 'Rocket: {} ({})'.format(self.vehicle_type, self.id)

    def as_dict(self):
        return {
            'rocket_id': self.id,
            'vehicle_type': self.vehicle_type
        }


class CustomerModel(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    customer_type = Column(String(120), nullable=False)
    country = Column(String(120), nullable=False)

    # flights = relationship("FlightModel", secondary="flight_customers", back_populates="customers")

    def __repr__(self):
        return '<Customer {}>'.format(self.id)

    def __str__(self):
        return 'Customer: {} ({})'.format(self.name, self.id)

    def as_dict(self):
        return {
            'customer_id': self.id,
            'name': self.name,
            'customer_type': self.customer_type,
            'country': self.country
        }


class CargoModel(Base):
    __tablename__ = 'cargos'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    payload_type = Column(String(120), nullable=False)
    mass = Column(Float, nullable=False)
    orbit = Column(String(120), nullable=False)

    # flights = relationship("FlightModel", secondary="flight_cargos", back_populates="cargos")

    def __repr__(self):
        return '<Cargo {}>'.format(self.id)

    def __str__(self):
        return 'Cargo: {} ({})'.format(self.name, self.id)

    def as_dict(self):
        return {
            'cargo_id': self.id,
            'name': self.name,
            'payload_type': self.payload_type,
            'mass': self.mass,
            'orbit': self.orbit
        }


# class FlightCustomers(Base):
#     __tablename__ = 'flight_customers'
#     flight_id = Column(Integer, ForeignKey("flights.id"), primary_key=True)
#     customer_id = Column(Integer, ForeignKey("customers.id"), primary_key=True)
#
#
# class FlightCargos(Base):
#     __tablename__ = 'flight_cargos'
#     flight_id = Column(Integer, ForeignKey("flights.id"), primary_key=True)
#     cargo_id = Column(Integer, ForeignKey("cargos.id"), primary_key=True)


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(120), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    date_created = Column(DateTime, default=func.now(), nullable=False)
    date_modified = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def __str__(self):
        return 'User: {} ({})'.format(self.username, self.email)

    def as_dict(self):
        return {
            'user_id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'date_created': self.date_created,
            'date_modified': self.date_modified
        }

    def check_password(self, password: str) -> bool:
        try:
            return bcrypt.checkpw(bytes(password, 'utf-8'), self.password.encode('utf-8'))
        except Exception as e:
            logging.error(f"Error checking password: {e}")
            raise Exception(f"Error checking password: {e}")


class JwtTokenModel(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    refresh_token = Column(String(120), unique=True, nullable=False)
    date_created = Column(DateTime, default=func.now(), nullable=False)
    date_modified = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return '<Token %r>' % self.refresh_token

    def __str__(self):
        return 'Token: {} ({})'.format(self.refresh_token, self.user_id)

    def as_dict(self):
        return {
            'token_id': self.id,
            'user_id': self.user_id,
            'refresh_token': self.refresh_token,
            'date_created': self.date_created,
            'date_modified': self.date_modified
        }
