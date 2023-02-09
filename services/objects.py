from typing import Optional


class Flight:
    def __init__(self, number, launch_date, flight_status, launch_time, launch_site, mission_outcome,
                 failure_reason, landing_type, landing_outcome, rocket_id=Optional[int], flight_id=Optional[int],
                 flight_record=None):
        self._id = flight_id
        self.number = number
        self.launch_date = launch_date
        self.flight_status = flight_status
        self.launch_time = launch_time
        self.launch_site = launch_site
        self.mission_outcome = mission_outcome
        self.failure_reason = failure_reason
        self.landing_type = landing_type
        self.landing_outcome = landing_outcome
        # self.rocket = rocket
        self.rocket_id = rocket_id
        # self.customers = customers
        # self.cargos = cargos
        self._flight_record = flight_record

    def __repr__(self):
        return f"<Flight(number={self.number})>"

    @property
    def id(self):
        return self._id or self._flight_record.id

    def dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'launch_date': self.launch_date,
            'flight_status': self.flight_status,
            'launch_time': self.launch_time,
            'launch_site': self.launch_site,
            'mission_outcome': self.mission_outcome,
            'failure_reason': self.failure_reason,
            'landing_type': self.landing_type,
            'landing_outcome': self.landing_outcome,
            'rocket_id': self.rocket,
            'customers': self.customers,
            'cargos': self.cargos
        }


class Rocket:
    def __init__(self, vehicle_type, rocket_id: Optional, flights: Optional = None, rocket_record=None):
        self._id = rocket_id
        self.vehicle_type = vehicle_type
        self.flights = flights
        self._rocket_record = rocket_record

    def __repr__(self):
        return f"<Rocket(vehicle_type={self.vehicle_type})>"

    @property
    def id(self):
        return self._id or self._rocket_record.id

    def dict(self):
        return {
            'rocket_id': self.id,
            'vehicle_type': self.vehicle_type,
            'flights': self.flights
        }


class Customer:
    def __init__(self, name, customer_type, country, customer_id: Optional[int], customer_record=None):
        self._id = customer_id
        self.name = name
        self.customer_type = customer_type
        self.country = country
        self._customer_record = customer_record

    def __repr__(self):
        return f"<Customer(name={self.name})>"

    @property
    def id(self):
        return self._id or self._customer_record.id

    def dict(self):
        return {
            'customer_id': self.id,
            'name': self.name,
            'customer_type': self.customer_type,
            'country': self.country
        }


class Cargo:
    def __init__(self, name, payload_type, mass, orbit, cargo_id: Optional[int] = None, cargo_record=None):
        self._id = cargo_id
        self.name = name
        self.payload_type = payload_type
        self.mass = mass
        self.orbit = orbit
        self._cargo_record = cargo_record

    def __repr__(self):
        return f"<Cargo(name={self.name})>"

    @property
    def id(self):
        return self._id or self._cargo_record.id

    def dict(self):
        return {
            'cargo_id': self.id,
            'name': self.name,
            'payload_type': self.payload_type,
            'mass': self.mass,
            'orbit': self.orbit
        }


class User:
    def __init__(self, username, email, password, date_created, date_modified, user_id: Optional[int] = None,
                 user_record=None):
        self._id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.date_created = date_created
        self.date_modified = date_modified
        self._user_record = user_record

    def __repr__(self):
        return f"<User(username={self.username})>"

    @property
    def id(self):
        return self._id or self._user_record.id

    def dict(self):
        return {
            'user_id': self.id,
            'username': self.username,
            'email': self.email,
            'date_created': self.date_created,
            'date_modified': self.date_modified
        }


class Token:
    def __init__(self, user_id: int, refresh_token: str, token_id: Optional[int] = None,
                 date_created: str = None, date_modified: str = None, token_record=None):
        self._id = token_id
        self.user_id = user_id
        self.refresh_token = refresh_token
        self._token_record = token_record
        self.date_created = date_created
        self.date_modified = date_modified

    def __repr__(self):
        return f"<Token(user_id={self.user_id})>"

    @property
    def id(self):
        return self._id or self._token_record.id

    def dict(self):
        return {
            'token_id': self.id,
            'user_id': self.user_id,
            'refresh_token': self.refresh_token,
        }
