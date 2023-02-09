from marshmallow import Schema, fields, validate, EXCLUDE


class UpdateUserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    username = fields.String(required=True)
    email = fields.String(required=True)


class UserSchema(UpdateUserSchema):
    class Meta:
        unknown = EXCLUDE

    password = fields.String(required=True)


class GetUserSchema(UserSchema):
    id = fields.UUID(required=True)
    date_created = fields.DateTime()
    date_modified = fields.DateTime()


class CargoSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.String(required=True)
    payload_type = fields.String(required=True)
    mass = fields.Float(required=True)
    orbit = fields.String(required=True)


class GetCargoSchema(CargoSchema):
    class Meta:
        unknown = EXCLUDE

    id = fields.UUID(required=True)
    flight_id = fields.Nested('GetFlightSchema')


class RocketSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    vehicle_type = fields.String()


class GetRocketSchema(RocketSchema):
    class Meta:
        unknown = EXCLUDE

    id = fields.UUID(required=True)
    flights = fields.Nested('GetFlightSchema')


class CustomerSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.String()
    country = fields.String()
    customer_type = fields.String(
        required=True,
        validate=validate.OneOf(
            ['government', 'business']
        ),
    )


class GetCustomerSchema(CustomerSchema):
    class Meta:
        unknown = EXCLUDE

    id = fields.UUID(required=True)
    flight_id = fields.Nested('GetFlightSchema')


class FlightSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    customer_id = fields.List(fields.Int(), required=True)
    cargo_id = fields.List(fields.Int(), required=True)
    rocket_id = fields.Integer(required=True)
    flight_status = fields.String(
        validate=validate.OneOf(
            ['schedule', 'countdown', 'abort', 'launch']
        ),
    )
    number = fields.String()
    launch_date = fields.String()
    launch_time = fields.String()
    launch_site = fields.String()
    mission_outcome = fields.String()
    failure_reason = fields.String()
    landing_type = fields.String(
        required=True,
        validate=validate.OneOf(
            ['parachute', 'ocean', 'ship', 'land', 'none']
        ),
    )
    landing_outcome = fields.String()


class GetFlightSchema(FlightSchema):
    class Meta:
        unknown = EXCLUDE

    id = fields.UUID(required=True)
    rocket = fields.Nested(GetRocketSchema)
    customers = fields.Nested(GetCustomerSchema)
    cargos = fields.Nested(GetCargoSchema)


class QueryFlightSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    from_date = fields.DateTime()
    to_date = fields.DateTime()
    customer = fields.String()
    rocket_type = fields.Nested(RocketSchema, only=('vehicle_type',))
    limit = fields.Integer(default=10)


class UploadCSVorXLSArgs(Schema):
    file = fields.Field(required=True)
    sheet_index = fields.Int(missing=0,
                             description="Index of the sheet in the file to be processed")
    header_row = fields.Int(missing=0,
                            description="Row number that contains the header information in the sheet")
    should_preview = fields.Bool(missing=False,
                                 description="Flag indicating whether to return a preview of the data or to actually process the data")


class RefreshTokenSchema(Schema):
    refresh_token = fields.String(required=True)


class TokenSchema(Schema):
    access_token = fields.String(required=True)
    refresh_token = fields.String(required=True)


class LoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
